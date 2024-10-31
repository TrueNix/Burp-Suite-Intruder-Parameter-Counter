# -*- coding: utf-8 -*-
from burp import IBurpExtender, IHttpListener, ITab, IMessageEditorController
from javax.swing import JPanel, JTextField, JLabel, JButton, JList, JScrollPane, DefaultListModel
from java.awt import BorderLayout, FlowLayout
import re

class BurpExtender(IBurpExtender, IHttpListener, ITab, IMessageEditorController):

    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        self.callbacks.setExtensionName("Intruder Parameter Counter")

        # Main config panel for adding/removing parameters
        self.config_panel = JPanel(BorderLayout())

        # List model to store parameters
        self.parameter_list_model = DefaultListModel()
        self.parameter_list = JList(self.parameter_list_model)

        # Scroll pane for the list of parameters
        list_scroll = JScrollPane(self.parameter_list)
        self.config_panel.add(list_scroll, BorderLayout.CENTER)

        # Panel for input and buttons
        input_panel = JPanel(FlowLayout())

        # Text field for new parameter input
        self.parameterField = JTextField(15)
        input_panel.add(JLabel("Parameter to count:"))
        input_panel.add(self.parameterField)

        # Add and remove buttons
        add_button = JButton("Add Parameter", actionPerformed=self.add_parameter)
        remove_button = JButton("Remove Selected", actionPerformed=self.remove_parameter)
        input_panel.add(add_button)
        input_panel.add(remove_button)

        # Add input panel to the main panel
        self.config_panel.add(input_panel, BorderLayout.SOUTH)

        # Register this panel as a custom tab in Burp
        self.callbacks.customizeUiComponent(self.config_panel)
        self.callbacks.addSuiteTab(self)

        # Register HTTP listener
        callbacks.registerHttpListener(self)

        # Dictionary to store the parameters
        self.parameters = []

        # Track the current message for IMessageEditorController
        self.current_message = None

        return

    def getTabCaption(self):
        return "Intruder Parameter Counter"

    def getUiComponent(self):
        return self.config_panel

    def add_parameter(self, event):
        # Add parameter from text field to list if it’s not already in the list
        parameter = self.parameterField.getText().strip()
        if parameter and not self.parameter_list_model.contains(parameter):
            self.parameter_list_model.addElement(parameter)
            self.parameters.append(parameter)
            self.callbacks.printOutput("Added parameter: '{}'".format(parameter))
        self.parameterField.setText("")

    def remove_parameter(self, event):
        # Remove selected parameter(s) from list
        selected_parameters = self.parameter_list.getSelectedValuesList()
        for parameter in selected_parameters:
            self.parameter_list_model.removeElement(parameter)
            self.parameters.remove(parameter)
            self.callbacks.printOutput("Removed parameter: '{}'".format(parameter))

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # Process only Intruder responses
        if toolFlag == self.callbacks.TOOL_INTRUDER and not messageIsRequest:
            response = messageInfo.getResponse()
            response_info = self.helpers.analyzeResponse(response)
            response_body = response[response_info.getBodyOffset():].tostring()

            # Count occurrences of each parameter and prepare a message
            count_message = ""
            for parameter in self.parameters:
                count = len(re.findall(parameter, response_body))
                count_message += "Occurrences of '{}': {}\n ".format(parameter, count)

            # Set the current message for IMessageEditorController
            self.current_message = count_message.encode()

            # Create a custom message editor to display the count results
            message_editor = self.callbacks.createMessageEditor(self, False)
            message_editor.setMessage(self.current_message, False)

            # Set the count summary as a comment for the Intruder result
            messageInfo.setComment(count_message.strip())

            # Log the count summary in the Extender output tab
            self.callbacks.printOutput("Parameter counts in Intruder response:\n{}".format(count_message))

    # IMessageEditorController methods
    def getHttpService(self):
        return None

    def getRequest(self):
        return None

    def getResponse(self):
        # Provide the custom message for the editor
        return self.current_message
