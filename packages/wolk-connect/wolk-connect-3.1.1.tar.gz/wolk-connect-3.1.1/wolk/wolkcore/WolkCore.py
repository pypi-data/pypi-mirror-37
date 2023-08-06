#   Copyright 2018 WolkAbout Technology s.r.o.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from wolk.wolkcore import SensorReading
from wolk.wolkcore import Alarm
from wolk.wolkcore import ActuatorCommandType
from wolk.wolkcore import ActuatorStatus
from wolk.wolkcore import ConfigurationCommandType
from wolk.wolkcore import FirmwareCommandType
from wolk.wolkcore import FirmwareStatus
from wolk.wolkcore import FirmwareStatusType
from wolk.wolkcore import FirmwareErrorType

"""
WolkCore Module.
"""


class WolkCore:
    """WolkCore ties together all the functionality of WolkConnect library."""

    def __init__(
        self,
        outbound_message_factory,
        outbound_message_queue,
        connectivity_service,
        actuation_handler,
        actuator_status_provider,
        inbound_message_deserializer,
        configuration_handler,
        configuration_provider,
        keep_alive_service=None,
        firmware_update=None,
    ):
        """
        Core of WolkConnect library.

        :param outbound_message_factory: Serialize messages to be sent to WolkAbout IoT Platform
        :type outbound_message_factory: wolk.wolkcore.OutboundMessageFactory.OutboundMessageFactory
        :param outbound_message_queue: Store messages that are ready to be sent
        :type outbound_message_queue: wolk.wolkcore.OutboundMessageQueue.OutboundMessageQueue
        :param connectivity_service: Provide communication with WolkAbout IoT Platform
        :type connectivity_service: wolk.wolkcore.ConnectivityService.ConnectivityService
        :param actuation_handler: Execute actuation commands issued from WolkAbout IoT Platform
        :type actuation_handler: wolk.ActuationHandler.ActuationHandler
        :param actuator_status_provider: Report current actuator status to WolkAbout IoT Platform
        :type actuator_status_provider: wolk.ActuatorStatusProvider.ActuatorStatusProvider
        :param inbound_message_deserializer: Deserialize messages received from WolkAbout IoT Platform
        :type inbound_message_deserializer: wolk.wolkcore.InboundMessageDeserializer.InboundMessageDeserializer
        :param configuration_handler: Execute configuration command received from WolkAbout IoT Platform
        :type configuration_handler: wolk.ConfigurationHandler.ConfigurationHandler
        :param configuration_provider: Report current configuration options to WolkAbout IoT Platform
        :type configuration_provider: wolk.ConfigurationProvider.ConfigurationProvider
        :param keep_alive_service: Maintain connection to WolkAbout IoT Platform
        :type keep_alive_service: wolk.wolkcore.KeepAliveService.KeepAliveService or None
        :param firmware_update: Update device's firmware from WolkAbout IoT Platform
        :type firmware_update:  wolk.wolkcore.FirmwareUpdate.FirmwareUpdate or None
        """
        self.outbound_message_factory = outbound_message_factory
        self.outbound_message_queue = outbound_message_queue
        self.connectivity_service = connectivity_service
        self.inbound_message_deserializer = inbound_message_deserializer
        self.actuation_handler = actuation_handler
        self.actuator_status_provider = actuator_status_provider
        self.configuration_handler = configuration_handler
        self.configuration_provider = configuration_provider
        self.connectivity_service.set_inbound_message_listener(
            self._on_inbound_message
        )

        self.keep_alive_service = None

        if keep_alive_service:
            self.keep_alive_service = keep_alive_service

        self.firmware_update = firmware_update

        if self.firmware_update:

            self.firmware_update.set_on_file_packet_request_callback(
                self._on_packet_request
            )
            self.firmware_update.set_on_status_callback(self._on_status)

    def connect(self):
        """Connect to WolkAbout IoT Platform and start keep alive service."""
        self.connectivity_service.connect()
        if self.keep_alive_service:
            self.keep_alive_service.start()

    def disconnect(self):
        """Disconnect from WolkAbout IoT Platform and stop keep alive service."""
        self.connectivity_service.disconnect()
        if self.keep_alive_service:
            self.keep_alive_service.stop()

    def add_sensor_reading(self, reference, value, timestamp=None):
        """
        Store a sensor reading to be sent to WolkAbout IoT Platform.

        :param reference: Reference of the sensor
        :type reference: str
        :param value: Value of the sensor reading
        :type value: int or float or str
        :param timestamp: Unix timestamp. If not provided, platform will assign
        :type timestamp: int
        """
        reading = SensorReading(reference, value, timestamp)
        outbound_message = self.outbound_message_factory.make_from_sensor_reading(
            reading
        )
        self.outbound_message_queue.put(outbound_message)

    def add_alarm(self, reference, active, timestamp=None):
        """
        Store an alarm state to be published the platform.

        :param reference: Reference of the alarm
        :type reference: str
        :param active: Current state of the alarm
        :type active: bool
        :param timestamp: Unix timestamp. If not provided, platform will assign
        :type timestamp: int or None
        """
        alarm = Alarm(reference, active, timestamp)
        outbound_message = self.outbound_message_factory.make_from_alarm(alarm)
        self.outbound_message_queue.put(outbound_message)

    def publish(self):
        """Publish all currently stored messages to WolkAbout IoT Platform."""
        while True:
            outbound_message = self.outbound_message_queue.peek()

            if outbound_message is None:

                break

            if self.connectivity_service.publish(outbound_message) is True:

                self.outbound_message_queue.get()

            else:

                break

    def publish_actuator_status(self, reference):
        """
        Publish the current actuator status to the platform.

        :param reference: Reference of the actuator
        :type reference: str
        """
        state, value = self.actuator_status_provider.get_actuator_status(
            reference
        )
        actuator_status = ActuatorStatus(reference, state, value)
        outbound_message = self.outbound_message_factory.make_from_actuator_status(
            actuator_status
        )

        if not self.connectivity_service.publish(outbound_message):
            self.outbound_message_queue.put(outbound_message)

    def publish_configuration(self):
        """Publish the current device configuration to the platform."""
        configuration = self.configuration_provider.get_configuration()
        outbound_message = self.outbound_message_factory.make_from_configuration(
            configuration
        )

        if not self.connectivity_service.publish(outbound_message):
            self.outbound_message_queue.put(outbound_message)

    def _on_inbound_message(self, message):
        """
        Handle inbound messages.

        .. note:: Pass this function to the implementation of ConnectivityService
        :param message: The message received from the platform
        :type message: wolk.wolkcore.InboundMessage.InboundMessage
        """
        if message.channel.startswith("actuators/commands/"):

            if not self.actuation_handler or not self.actuator_status_provider:
                return

            actuation = self.inbound_message_deserializer.deserialize_actuator_command(
                message
            )

            if (
                actuation.command
                == ActuatorCommandType.ACTUATOR_COMMAND_TYPE_SET
            ):

                self.actuation_handler.handle_actuation(
                    actuation.reference, actuation.value
                )

                self.publish_actuator_status(actuation.reference)

            elif (
                actuation.command
                == ActuatorCommandType.ACTUATOR_COMMAND_TYPE_STATUS
            ):

                self.publish_actuator_status(actuation.reference)

        elif message.channel.startswith("service/commands/firmware/"):

            if not self.firmware_update:
                # Firmware update disabled
                firmware_status = FirmwareStatus(
                    FirmwareStatusType.FIRMWARE_STATUS_ERROR,
                    FirmwareErrorType.FIRMWARE_ERROR_FILE_UPLOAD_DISABLED,
                )
                outbound_message = self.outbound_message_factory.make_from_firmware_status(
                    firmware_status
                )
                if not self.connectivity_service.publish(outbound_message):
                    self.outbound_message_queue.put(outbound_message)
                return

            firmware_command = self.inbound_message_deserializer.deserialize_firmware_command(
                message
            )

            if (
                firmware_command.command
                == FirmwareCommandType.FIRMWARE_COMMAND_TYPE_FILE_UPLOAD
            ):

                self.firmware_update.handle_file_upload(firmware_command)

            elif (
                firmware_command.command
                == FirmwareCommandType.FIRMWARE_COMMAND_TYPE_URL_DOWNLOAD
            ):

                self.firmware_update.handle_url_download(firmware_command)

            elif (
                firmware_command.command
                == FirmwareCommandType.FIRMWARE_COMMAND_TYPE_INSTALL
            ):

                self.firmware_update.handle_install()

            elif (
                firmware_command.command
                == FirmwareCommandType.FIRMWARE_COMMAND_TYPE_ABORT
            ):

                self.firmware_update.handle_abort()

            elif (
                firmware_command.command
                == FirmwareCommandType.FIRMWARE_COMMAND_TYPE_UNKNOWN
            ):
                pass

        elif message.channel.startswith("service/binary/"):

            if not self.firmware_update:
                # Firmware update disabled
                firmware_status = FirmwareStatus(
                    FirmwareStatusType.FIRMWARE_STATUS_ERROR,
                    FirmwareErrorType.FIRMWARE_ERROR_FILE_UPLOAD_DISABLED,
                )
                outbound_message = self.outbound_message_factory.make_from_firmware_status(
                    firmware_status
                )
                if not self.connectivity_service.publish(outbound_message):
                    self.outbound_message_queue.put(outbound_message)
                return

            packet = self.inbound_message_deserializer.deserialize_firmware_chunk(
                message
            )
            self.firmware_update.handle_packet(packet)

        elif message.channel.startswith("configurations/commands/"):

            if (
                not self.configuration_provider
                or not self.configuration_handler
            ):
                return

            configuration = self.inbound_message_deserializer.deserialize_configuration_command(
                message
            )

            if (
                configuration.command
                == ConfigurationCommandType.CONFIGURATION_COMMAND_TYPE_SET
            ):
                self.configuration_handler.handle_configuration(
                    configuration.values
                )
                self.publish_configuration()

            elif (
                configuration.command
                == ConfigurationCommandType.CONFIGURATION_COMMAND_TYPE_CURRENT
            ):
                self.publish_configuration()

    def _on_packet_request(self, file_name, chunk_index, chunk_size):
        """
        Handle firmware packet request.

        :param file_name: Firmware file name
        :type file_name: str
        :param chunk_index: Index of requested firmware file chunk
        :type chunk_index: int
        :param chunk_size: Size of firmware file chunk in bytes
        :type chunk_size: int
        """
        message = self.outbound_message_factory.make_from_chunk_request(
            file_name, chunk_index, chunk_size
        )
        if not self.connectivity_service.publish(message):
            self.outbound_message_queue.put(message)

    def _on_status(self, status):
        """
        Report firmware update status.

        :param status: Current firmware update status
        :type status: wolk.wolkcore.FirmwareStatus.FirmwareStatus
        """
        message = self.outbound_message_factory.make_from_firmware_status(
            status
        )
        if not self.connectivity_service.publish(message):
            self.outbound_message_queue.put(message)
