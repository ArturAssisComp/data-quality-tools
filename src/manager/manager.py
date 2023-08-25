from src.manager.models.manager_request  import ManagerRequest
from src.manager.models.user_request     import UserRequest
from src.manager.models.user_response    import UserResponse
from src.manager.models.manager_response import ManagerResponse
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
    user_request:UserRequest
    manager_request:ManagerRequest
    #-------------------------
    user_response:UserResponse
    manager_response:ManagerResponse
    #-------------------------
    output_path:str
    dataset: list[str]
    name:str
    description:str

    def _process_manager_arguments(self):
        manager_arguments = self.user_request.manager_arguments

        self.output_path = manager_arguments.output_path
        self.dataset = manager_arguments.dataset
        self.name = manager_arguments.name
        self.description = manager_arguments.description
    
    def _start_tools(self):
        # TODO start tools
        print('start tools')
        pass

    def process_user_request(self, user_request: UserRequest):
        self.user_request = user_request
        self.manager_request = ManagerRequest.from_user_request(self.user_request)

        self._process_manager_arguments()


        self._start_tools()
        # TODO receive manager response from each tool
        # TODO create user response from manager response

        
