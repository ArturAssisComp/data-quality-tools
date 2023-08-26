from manager.models.manager_arguments import ManagerArguments
'''
MANAGER 
- the manager will receive the user request and organize the response;
- each tool will generate a separate process;
- all the processes will only read the data, not write. This way, we do not need
to worry about race condition;
- each process will generate its results and send a message to the manager when
they are done;
- the manager will receive the messages and organize them for the response to the
final user;
'''




class Manager:
    manager_arguments: ManagerArguments

    def _process_manager_arguments(self):
        manager_arguments = self.manager_arguments

        self.output_path = manager_arguments.output_path
        self.dataset = manager_arguments.dataset
        self.name = manager_arguments.name
        self.description = manager_arguments.description
    
    def _start_tools(self):
        # TODO start tools
        print('start tools')
        pass

    def process_user_request(self, raw_user_request: dict):
        self.manager_arguments = ManagerArguments(**raw_user_request)
        print(f'Manager arguments: {self.manager_arguments}')

        self._process_manager_arguments()


        self._start_tools()
        # TODO receive manager response from each tool
        # TODO create user response from manager response

        
