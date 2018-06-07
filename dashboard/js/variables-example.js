// once this file has been amended, rename to variables.js so index.html will pick up the file
// ### in between the triple hashes comments is where you supply your environment-specific values
var cognitoIdentityPoolId = "replace"; // this value can be grabbed from the cloudformation output for your stack
var region = "replace"; // replace with whatever region your stack is deployed to 
var awsIotEndpointAddress = "replace"; // this value can be grabbed via the IoT Core console or via the CLI 
var mqttTopicName = "ipgeolocator/publish";
// ###