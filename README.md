# Intruder Parameter Counter for Burp Suite

**Intruder Parameter Counter** is a Burp Suite extension designed to help security researchers and penetration testers automatically count occurrences of specified parameters in HTTP responses during Intruder attacks. This extension enables users to configure specific parameters to monitor within HTTP responses, displaying the counts in both custom response tabs and the Comments section of Intruder results.

### Features

- **Parameter Tracking**: Configure a list of parameters to track within HTTP responses. This is particularly useful for observing patterns in responses during large-scale Intruder attacks.
- **Count Summary in Intruder Results**: Displays a summary of parameter counts directly in the **Comments** column of Intruder results for easy reference.
- **Custom Response Display**: Creates a custom response preview in the Intruder response view, showcasing the counts of each parameter within the response content.
- **User-Friendly Configuration**: Simple GUI for adding or removing parameters to track, making it flexible and easy to adapt to different scenarios.

### Installation

1. **Clone or Download** the repository.
2. **Add the Extension**:
   - Open **Burp Suite**.
   - Navigate to **Extender > Extensions**.
   - Click **Add** and load the `counter.py` file.
3. Ensure **Python** and **Jython** are set up if using the Jython loader in Burp.

### Usage

1. Go to the **Intruder Parameter Counter** tab in Burp Suite.
2. Use the text box to add parameters that you wish to track in Intruder responses. You can also remove parameters as needed.
3. Start an Intruder attack. For each response, the extension will:
   - Display the parameter counts in the **Comments** column within the Intruder results table.
   - Show parameter counts in a custom response view for each Intruder result.
4. Check the **Extender** output tab for logs showing parameter counts for each response.

### Example Use Case

Suppose you're testing for responses that include multiple instances of a particular keyword or identifier, like `"image_versions2"`. By adding this keyword in **Intruder Parameter Counter**, the extension will automatically detect and count occurrences in each response, saving time and improving accuracy for large-scale Intruder tests.

### Contributing

Feel free to submit issues, feature requests, or pull requests to improve the extension. Contributions are always welcome!

### License

This project is licensed under the MIT License.
