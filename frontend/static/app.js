function Device(device_id) {
    var self = this;
    self.id = device_id
    self.messages = [];

    self.addMessage = function(message, is_user) {
        self.messages.push({
            content: message,
            is_user: is_user
        });
    };
}

function DeviceViewModel() {
    var self = this;
    self.headers = ko.observableArray([]);
    self.entries = ko.observableArray([]);
    self.ids = null
    self.connected = ko.observable(false)
    self.devices = []
    self.userInput = ko.observable("")
    self.currentDevice = ko.observable(new Device(-1))

    self.loadDevices = function() {
        $.ajax({
            url: "/api/devices",
            type: "GET",
            success: function(data){
                self.connected(true);
                data = JSON.parse(data);
                if(Object.keys(data).length === 0)
                    return;

                self.ids=data.index
                self.headers(data.columns);
                self.entries(data.data)
                for(let i=0;i<self.ids.length;i++)
                {
                    self.devices.push(new Device(self.ids[i]))
                }
            }
        });
    };
    self.selectDevice = function(context,index) {
        /*$('#terminalModal').modal('show');
         self.currentDevice(self.devices[index])*/
        /*$.ajax({
            url: `/api/devices/${self.ids[index]}/prompt`,
            type: "GET",
            success: function(data){
                dev = new Device(2)
                dev.label = JSON.parse(data)
                self.device(dev)
            }
        })*/
    };

    self.handleKeyPress = function(data, event) {
        if (event.keyCode === 13) {
          var userInput = self.userInput().trim();
          if (userInput !== '') {
            self.currentDevice().addMessage(userInput,1);
          }
        }
        return true;
    };

    self.deselectDevice = function(context,index) {
        /* self.device(new Device(-1)) */
    };
    self.loadDevices();
}
dvm = new DeviceViewModel();
ko.applyBindings(dvm);
$('#terminalModal').on('hidden.bs.modal', dvm.deselectDevice);

