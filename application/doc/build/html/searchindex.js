Search.setIndex({docnames:["client","client_app","common","index","launcher","launcher_ubuntu","log","server","server_app","unit_tests"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["client.rst","client_app.rst","common.rst","index.rst","launcher.rst","launcher_ubuntu.rst","log.rst","server.rst","server_app.rst","unit_tests.rst"],objects:{"":[[0,0,0,"-","client"],[1,0,0,"-","client_app"],[2,0,0,"-","common"],[4,0,0,"-","launcher"],[5,0,0,"-","launcher_ubuntu"],[6,0,0,"-","log"],[7,0,0,"-","server"],[8,0,0,"-","server_app"],[9,0,0,"-","unit_tests"]],"client.client_db":[[0,1,1,"","ClientDB"]],"client.client_db.ClientDB":[[0,1,1,"","Base"],[0,1,1,"","Contacts"],[0,1,1,"","KnownUsers"],[0,1,1,"","MessageHistory"],[0,3,1,"","add_contact"],[0,3,1,"","add_users"],[0,3,1,"","check_contact"],[0,3,1,"","check_user"],[0,3,1,"","contacts_clear"],[0,3,1,"","del_contact"],[0,3,1,"","get_contacts"],[0,3,1,"","get_history"],[0,3,1,"","get_users"],[0,3,1,"","save_message"]],"client.client_db.ClientDB.Base":[[0,2,1,"","metadata"],[0,2,1,"","registry"]],"client.client_db.ClientDB.Contacts":[[0,2,1,"","id"],[0,2,1,"","name"]],"client.client_db.ClientDB.KnownUsers":[[0,2,1,"","id"],[0,2,1,"","username"]],"client.client_db.ClientDB.MessageHistory":[[0,2,1,"","contact"],[0,2,1,"","date"],[0,2,1,"","direction"],[0,2,1,"","id"],[0,2,1,"","message"]],"client.dialog_add_contact":[[0,1,1,"","AddContactDialog"]],"client.dialog_add_contact.AddContactDialog":[[0,3,1,"","possible_contacts_update"],[0,3,1,"","update_possible_users"]],"client.dialog_del_contact":[[0,1,1,"","DelContactDialog"]],"client.dialog_start":[[0,1,1,"","UserNameDialog"]],"client.dialog_start.UserNameDialog":[[0,3,1,"","click"]],"client.main_window":[[0,1,1,"","ClientMainWindow"]],"client.main_window.ClientMainWindow":[[0,3,1,"","add_contact"],[0,3,1,"","add_contact_action"],[0,3,1,"","add_contact_window"],[0,3,1,"","clients_list_update"],[0,3,1,"","connection_lost"],[0,3,1,"","delete_contact"],[0,3,1,"","delete_contact_window"],[0,3,1,"","history_list_update"],[0,3,1,"","make_connection"],[0,3,1,"","message"],[0,3,1,"","select_active_user"],[0,3,1,"","send_message"],[0,3,1,"","set_active_user"],[0,3,1,"","set_disabled_input"],[0,3,1,"","signal_205"]],"client.main_window_ui":[[0,1,1,"","Ui_MainClientWindow"]],"client.main_window_ui.Ui_MainClientWindow":[[0,3,1,"","retranslateUi"],[0,3,1,"","setupUi"]],"client.transport":[[0,1,1,"","ClientTransport"]],"client.transport.ClientTransport":[[0,3,1,"","add_contact"],[0,3,1,"","connection_init"],[0,2,1,"","connection_lost"],[0,3,1,"","contacts_list_request"],[0,3,1,"","create_presence"],[0,3,1,"","key_request"],[0,2,1,"","message_205"],[0,2,1,"","new_message"],[0,3,1,"","process_answ"],[0,3,1,"","remove_contact"],[0,3,1,"","run"],[0,3,1,"","send_message"],[0,3,1,"","transport_shutdown"],[0,3,1,"","user_list_request"]],"common.decos":[[2,4,1,"","log"],[2,4,1,"","login_required"]],"common.descrptrs":[[2,1,1,"","Port"]],"common.errors":[[2,5,1,"","IncorrectDataReceivedError"],[2,5,1,"","MissingClient"],[2,5,1,"","NonDictInputError"],[2,5,1,"","ReqFieldMissingError"],[2,5,1,"","ServerError"]],"common.metaclasses":[[2,1,1,"","ClientMaker"],[2,1,1,"","ServerMaker"]],"server.dialog_add_user":[[7,1,1,"","RegisterUser"]],"server.dialog_add_user.RegisterUser":[[7,3,1,"","save_data"]],"server.dialog_config":[[7,1,1,"","ConfigWindow"]],"server.dialog_config.ConfigWindow":[[7,3,1,"","init_ui"],[7,3,1,"","open_file_dialog"],[7,3,1,"","save_server_config"]],"server.dialog_remove_user":[[7,1,1,"","DeleteUserDialog"]],"server.dialog_remove_user.DeleteUserDialog":[[7,3,1,"","all_users_fill"],[7,3,1,"","remove_user"]],"server.main_window":[[7,1,1,"","MainWindow"]],"server.main_window.MainWindow":[[7,3,1,"","create_users_models"],[7,3,1,"","register_user"],[7,3,1,"","remove_user"],[7,3,1,"","server_config"],[7,3,1,"","show_statistics"]],"server.server_core":[[7,1,1,"","Server"]],"server.server_core.Server":[[7,3,1,"","init_socket"],[7,2,1,"","port"],[7,3,1,"","process_client_message"],[7,3,1,"","process_message"],[7,3,1,"","remove_client"],[7,3,1,"","run"],[7,3,1,"","service_update_lists"],[7,3,1,"","user_authorization"]],"server.server_db":[[7,1,1,"","ServerDB"]],"server.server_db.ServerDB":[[7,1,1,"","ActiveUsers"],[7,1,1,"","AllUsers"],[7,1,1,"","Base"],[7,1,1,"","LoginHistory"],[7,1,1,"","UsersContacts"],[7,1,1,"","UsersMessageStat"],[7,3,1,"","active_users_list"],[7,3,1,"","add_contact"],[7,3,1,"","add_user"],[7,3,1,"","check_user"],[7,3,1,"","get_contacts"],[7,3,1,"","get_password"],[7,3,1,"","get_public_key"],[7,3,1,"","message_statistic"],[7,3,1,"","process_message"],[7,3,1,"","remove_contact"],[7,3,1,"","remove_user"],[7,3,1,"","user_login"],[7,3,1,"","user_login_history"],[7,3,1,"","user_logout"],[7,3,1,"","users_list"]],"server.server_db.ServerDB.ActiveUsers":[[7,2,1,"","id"],[7,2,1,"","ip"],[7,2,1,"","port"],[7,2,1,"","time_conn"],[7,2,1,"","user"]],"server.server_db.ServerDB.AllUsers":[[7,2,1,"","id"],[7,2,1,"","last_conn"],[7,2,1,"","login"],[7,2,1,"","password"],[7,2,1,"","public_key"]],"server.server_db.ServerDB.Base":[[7,2,1,"","metadata"],[7,2,1,"","registry"]],"server.server_db.ServerDB.LoginHistory":[[7,2,1,"","id"],[7,2,1,"","ip"],[7,2,1,"","last_conn"],[7,2,1,"","port"],[7,2,1,"","user"]],"server.server_db.ServerDB.UsersContacts":[[7,2,1,"","contact"],[7,2,1,"","id"],[7,2,1,"","user"]],"server.server_db.ServerDB.UsersMessageStat":[[7,2,1,"","id"],[7,2,1,"","receive"],[7,2,1,"","sent"],[7,2,1,"","user"]],"server.stat_window":[[7,1,1,"","StatisticWindow"]],"server.stat_window.StatisticWindow":[[7,3,1,"","create_stat_model"],[7,3,1,"","init_ui"]],"unit_tests.test_utils":[[9,1,1,"","TestSocket"],[9,1,1,"","TestUtils"]],"unit_tests.test_utils.TestSocket":[[9,3,1,"","recv"],[9,3,1,"","send"]],"unit_tests.test_utils.TestUtils":[[9,2,1,"","error_dict"],[9,2,1,"","success_dict"],[9,2,1,"","test_dict_send"],[9,3,1,"","test_get_message_err"],[9,3,1,"","test_get_message_ok"],[9,3,1,"","test_get_tcp_parameters_address"],[9,3,1,"","test_get_tcp_parameters_default_address"],[9,3,1,"","test_get_tcp_parameters_default_port"],[9,3,1,"","test_get_tcp_parameters_default_server_address"],[9,3,1,"","test_get_tcp_parameters_port"],[9,3,1,"","test_get_tcp_parameters_returned_type"],[9,3,1,"","test_send_message"],[9,3,1,"","test_send_message_raise"]],client:[[0,0,0,"-","client_db"],[0,0,0,"-","dialog_add_contact"],[0,0,0,"-","dialog_del_contact"],[0,0,0,"-","dialog_start"],[0,0,0,"-","main_window"],[0,0,0,"-","main_window_ui"],[0,0,0,"-","transport"]],common:[[2,0,0,"-","decos"],[2,0,0,"-","descrptrs"],[2,0,0,"-","errors"],[2,0,0,"-","metaclasses"],[2,0,0,"-","utils"],[2,0,0,"-","variables"]],launcher_ubuntu:[[5,4,1,"","get_subprocess"]],log:[[6,0,0,"-","client_log_config"],[6,0,0,"-","server_log_config"]],server:[[7,0,0,"-","dialog_add_user"],[7,0,0,"-","dialog_config"],[7,0,0,"-","dialog_remove_user"],[7,0,0,"-","main_window"],[7,0,0,"-","server_core"],[7,0,0,"-","server_db"],[7,0,0,"-","stat_window"]],server_app:[[8,4,1,"","main"],[8,4,1,"","start_server_gui"]],unit_tests:[[9,0,0,"-","test_utils"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","function","Python function"],"5":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:function","5":"py:exception"},terms:{"1":[1,9],"123":1,"123456":1,"168":1,"192":1,"200":9,"2048":1,"205":7,"3":1,"400":9,"67348716":5,"8001":1,"8080":8,"\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u0438":7,"\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0430\u0446\u0438\u044e":[2,7],"\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445":2,"\u0430\u0432\u0442\u043e\u0440\u0438\u0437\u043e\u0432\u0430\u043d":2,"\u0430\u0434\u0440\u0435\u0441":[1,7,8],"\u0430\u0434\u0440\u0435\u0441\u0430":9,"\u0430\u0434\u0440\u0435\u0441\u0443":1,"\u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0433\u043e":0,"\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0445":7,"\u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u0430":1,"\u0430\u0440\u0433\u0435\u043c\u0435\u043d\u0442\u044b":8,"\u0430\u0440\u0433\u0443\u043c\u0435\u043d\u0442":2,"\u0430\u0440\u0433\u0443\u043c\u0435\u043d\u0442\u044b":1,"\u0431\u0430\u0437\u0435":0,"\u0431\u0430\u0437\u043e\u0439":0,"\u0431\u0430\u0437\u0443":[0,7],"\u0431\u0430\u0437\u044b":[0,7,8],"\u0431\u0434":0,"\u0431\u0435\u0437":8,"\u0431\u0443\u0434\u0435\u0442":9,"\u0431\u0443\u0434\u0443\u0442":1,"\u0431\u0443\u043b\u0435\u0432\u043e":0,"\u0432":[0,1,2,7,8,9],"\u0432\u0432\u0435\u0434\u0435\u043d\u044b":1,"\u0432\u0432\u043e\u0434\u0430":[0,7],"\u0432\u0432\u043e\u0434\u043e\u043c":0,"\u0432\u0437\u0430\u0438\u043c\u043e\u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0435":0,"\u0432\u0438\u0434\u0435":7,"\u0432\u043e\u0437\u0432\u0440\u0430\u0449\u0430\u0435\u043c\u044b\u0445":9,"\u0432\u043e\u0437\u043c\u043e\u0436\u043d\u044b\u0445":0,"\u0432\u0440\u0435\u043c\u044f":7,"\u0432\u0441\u0435":1,"\u0432\u0441\u0435\u043c\u0438":0,"\u0432\u0441\u0435\u0445":0,"\u0432\u0445\u043e\u0434":1,"\u0432\u0445\u043e\u0434\u0430":7,"\u0432\u0445\u043e\u0434\u0435":9,"\u0432\u0445\u043e\u0434\u043e\u0432":7,"\u0432\u044b\u0431\u043e\u0440\u0430":[0,7],"\u0432\u044b\u0434\u0430\u0435\u0442":0,"\u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f":7,"\u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0435\u0442":[0,7],"\u0432\u044b\u0445\u043e\u0434\u0435":[0,7],"\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u0443\u0435\u0442\u0441\u044f":2,"\u0433\u043b\u0430\u0432\u043d\u043e\u0433\u043e":7,"\u0433\u043b\u0430\u0432\u043d\u043e\u0435":[0,7],"\u0433\u0440\u0430\u0444\u0438\u0447\u0435\u0441\u043a\u043e\u0439":8,"\u0434\u0430\u043d\u043d\u043e\u0433\u043e":7,"\u0434\u0430\u043d\u043d\u043e\u043c":8,"\u0434\u0430\u043d\u043d\u044b\u0435":2,"\u0434\u0430\u043d\u043d\u044b\u0445":[0,7,8,9],"\u0434\u0430\u0442\u0430":0,"\u0434\u0432\u043e\u0439\u043d\u043e\u0439":0,"\u0434\u0435\u0430\u043a\u0442\u0438\u0432\u0438\u0440\u0443\u0435\u0442":0,"\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440":2,"\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440\u044b":2,"\u0434\u0435\u043a\u043e\u0440\u0438\u0440\u0443\u0435\u043c\u0430\u044f":2,"\u0434\u0435\u043a\u043e\u0440\u0438\u0440\u0443\u0435\u043c\u043e\u0439":2,"\u0434\u0435\u0441\u043a\u0440\u0438\u043f\u0442\u043e\u0440":[2,7],"\u0434\u0435\u0448\u0438\u0444\u0440\u043e\u0432\u043a\u0443":0,"\u0434\u0438\u0430\u043b\u043e\u0433":[0,7],"\u0434\u0438\u0430\u043b\u043e\u0433\u043e\u0432\u043e\u0435":7,"\u0434\u043b\u0438\u043d\u043d\u043e\u0439":1,"\u0434\u043b\u044f":[0,1,2,4,7,9],"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435":0,"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0438":0,"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f":0,"\u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u043d\u044b\u043c\u0438":0,"\u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u043c\u043e\u0433\u043e":[0,7],"\u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u043c\u044b\u0439":0,"\u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442":[0,7],"\u0435\u0433\u043e":7,"\u0435\u0441\u043b\u0438":[0,2,7],"\u0437\u0430":0,"\u0437\u0430\u0432\u0435\u0440\u0448\u0430\u0435\u0442":0,"\u0437\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u0438\u0435":8,"\u0437\u0430\u043a\u0440\u044b\u0432\u0430\u0435\u0442":0,"\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0438":8,"\u0437\u0430\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442":7,"\u0437\u0430\u043f\u0438\u0441\u044c":7,"\u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435":[0,7],"\u0437\u0430\u043f\u043e\u043b\u043d\u044f\u0435\u0442":[0,7],"\u0437\u0430\u043f\u0440\u0430\u0448\u0438\u0432\u0430\u0435\u0442":0,"\u0437\u0430\u043f\u0440\u043e\u0441":0,"\u0437\u0430\u043f\u0440\u043e\u0441\u0430":[0,2],"\u0437\u0430\u043f\u0443\u0441\u043a":[1,8],"\u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d":7,"\u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0445":7,"\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435":0,"\u0438":[0,1,2,7,9],"\u0438\u0437":[0,7,9],"\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u044b\u0445":[0,7],"\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0438":7,"\u0438\u043b\u0438":[0,1,7,8],"\u0438\u043c\u0435\u043d\u0438":0,"\u0438\u043c\u043c\u0438\u0442\u0430\u0446\u0438\u0438":9,"\u0438\u043c\u044f":[0,1,7],"\u0438\u043d\u0438\u0446\u0438\u0430\u043b\u0438\u0437\u0438\u0440\u0443\u0435\u0442":[0,7],"\u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435":[0,2],"\u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435":8,"\u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u044f":[1,8],"\u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c":1,"\u0438\u0441\u0442\u043e\u0440\u0438\u044e":[0,7],"\u0438\u0445":[0,7],"\u043a":[1,2],"\u043a\u043b\u0430\u0441\u0441":[0,7,9],"\u043a\u043b\u0430\u0441\u0441\u0430":[0,8],"\u043a\u043b\u0438\u0435\u043d\u0442":[1,2],"\u043a\u043b\u0438\u0435\u043d\u0442\u0430":[0,2,6,7],"\u043a\u043b\u0438\u0435\u043d\u0442\u0430\u043c":7,"\u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432":[2,7,8],"\u043a\u043b\u0438\u0435\u043d\u0442\u043e\u043c":2,"\u043a\u043b\u0438\u0435\u043d\u0442\u0441\u043a\u043e\u0435":1,"\u043a\u043b\u0438\u0435\u043d\u0442\u0443":7,"\u043a\u043b\u0438\u043a":0,"\u043a\u043b\u044e\u0447":[0,7],"\u043a\u043b\u044e\u0447\u0430":1,"\u043a\u043b\u044e\u0447\u0438":8,"\u043a\u043d\u043e\u043f\u043a\u0443":0,"\u043a\u043e\u0434\u0438\u0440\u0443\u0435\u0442":9,"\u043a\u043e\u0434\u043e\u043c":9,"\u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e":7,"\u043a\u043e\u043c\u0430\u043d\u0434\u0435":0,"\u043a\u043e\u043c\u0430\u043d\u0434\u043d\u043e\u0439":[1,8,9],"\u043a\u043e\u043c\u0430\u043d\u0434\u044b":8,"\u043a\u043e\u043c\u043c\u0430\u043d\u0434\u043d\u043e\u0439":1,"\u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442":7,"\u043a\u043e\u043d\u0441\u0442\u0430\u043d\u0442\u044b":2,"\u043a\u043e\u043d\u0442\u0430\u043a\u0442":[0,7],"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0430":[0,7],"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u043e\u0432":[0,7],"\u043a\u043e\u043d\u0442\u0430\u043a\u0442\u0443":0,"\u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438":7,"\u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f":[6,8],"\u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e\u0441\u0442\u0438":2,"\u043a\u043e\u0440\u0442\u0435\u0436\u0435\u0439":[0,7],"\u043a\u043e\u0442\u043e\u0440\u043e\u0433\u043e":[7,8],"\u043a\u043e\u0442\u043e\u0440\u043e\u043c":8,"\u043a\u043e\u0442\u043e\u0440\u043e\u043c\u0443":1,"\u043a\u043e\u0442\u043e\u0440\u044b\u0435":1,"\u043a\u043e\u0442\u043e\u0440\u044b\u0439":[0,2,7],"\u043a\u043e\u0442\u043e\u0440\u044b\u043c":[1,7],"\u043a\u0440\u043e\u043c\u0435":2,"\u043b\u0430\u0443\u043d\u0447\u0435\u0440":4,"\u043b\u0438":0,"\u043b\u043e\u0433\u0433\u0435\u0440\u0430":6,"\u043b\u043e\u0433\u0433\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f":2,"\u043c\u0435\u0436\u0434\u0443":0,"\u043c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440\u0430":8,"\u043c\u0435\u0442\u0430\u043a\u043b\u0430\u0441\u0441":2,"\u043c\u0435\u0442\u0430\u043a\u043b\u0430\u0441\u0441\u044b":2,"\u043c\u0435\u0442\u043e\u0434":0,"\u043c\u043e\u0434\u0443\u043b\u044c":8,"\u043d\u0430":[0,2,7,8,9],"\u043d\u0430\u0439\u0434\u0435\u043d":2,"\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435":0,"\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u044f\u043d\u0438\u0435":0,"\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438":[2,7],"\u043d\u0430\u0445\u043e\u0434\u0438\u0442\u0441\u044f":2,"\u043d\u0430\u0445\u043e\u0434\u044f\u0442\u0441\u044f":1,"\u043d\u0435":[0,2,7,9],"\u043d\u0435\u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u044b\u0435":2,"\u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e":1,"\u043d\u0435\u043e\u0431\u0445\u043e\u0434\u0438\u043c\u043e\u0441\u0442\u0438":7,"\u043d\u0435\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u044b\u043c\u0438":1,"\u043d\u043e":1,"\u043d\u043e\u0432\u043e\u0433\u043e":[0,7],"\u043e":[0,7],"\u043e\u0431":[0,7],"\u043e\u0431\u043c\u0435\u043d\u0430":1,"\u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c":7,"\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435":0,"\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u044f":0,"\u043e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u0442":[0,7],"\u043e\u0431\u043d\u043e\u0432\u043b\u044f\u044e\u0442":0,"\u043e\u0431\u043e\u043b\u043e\u0447\u043a\u0438":8,"\u043e\u0431\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u0435\u0442":[0,7,8],"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443":7,"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a":8,"\u043e\u0431\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0430":8,"\u043e\u0431\u0440\u0430\u0449\u0435\u043d\u0438\u0435":2,"\u043e\u0431\u0449\u0438\u0435":2,"\u043e\u0431\u044a\u0435\u043a\u0442":[0,2],"\u043e\u0431\u044a\u0435\u043a\u0442\u043d\u043e":8,"\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435":2,"\u043e\u043a":0,"\u043e\u043a\u043d\u0430":[0,7],"\u043e\u043a\u043d\u0435":[1,7],"\u043e\u043a\u043d\u043e":[0,7],"\u043e\u043a\u043e\u043d":8,"\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u044f":[2,7],"\u043e\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442":7,"\u043e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u043d\u043e\u043c\u0443":7,"\u043e\u043f\u0446\u0438\u0438":1,"\u043e\u0440\u0438\u0435\u043d\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439":8,"\u043e\u0441\u043d\u043e\u0432\u043d\u0430\u044f":8,"\u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0435":0,"\u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439":[0,7],"\u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445":8,"\u043e\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442":8,"\u043e\u0441\u0443\u0449\u0435\u0441\u0442\u0432\u043b\u044f\u0435\u0442":[0,7,8],"\u043e\u0442":[0,2,7],"\u043e\u0442\u0432\u0435\u0442":0,"\u043e\u0442\u0432\u0435\u0447\u0430\u044e\u0449\u0435\u0433\u043e":0,"\u043e\u0442\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435":7,"\u043e\u0442\u043a\u0440\u044b\u0432\u0448\u0435\u043c\u0441\u044f":1,"\u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f":7,"\u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f":7,"\u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438":9,"\u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0443":[1,7],"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u044b\u0445":7,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e":9,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c\u043e\u0435":9,"\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442":[0,7],"\u043e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442":2,"\u043e\u0447\u0438\u0449\u0430\u0435\u0442":0,"\u043e\u0448\u0438\u0431\u043a\u0430":2,"\u043e\u0448\u0438\u0431\u043a\u0435":0,"\u043e\u0448\u0438\u0431\u043a\u0438":[2,9],"\u043f\u0430\u043f\u043a\u0438":7,"\u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u0430\u043c\u0438":1,"\u043f\u0430\u0440\u0435":1,"\u043f\u0430\u0440\u043e\u043b\u0435\u043c":1,"\u043f\u0430\u0440\u043e\u043b\u044c":1,"\u043f\u0430\u0440\u043e\u043b\u044f":7,"\u043f\u0435\u0440\u0435\u0434\u0430\u0435\u0442":7,"\u043f\u0435\u0440\u0435\u0434\u0430\u043d\u043e":7,"\u043f\u0435\u0440\u0435\u0434\u0430\u0447\u0438":7,"\u043f\u043a":7,"\u043f\u043e":[0,1,9],"\u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442":1,"\u043f\u043e\u0434\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u044e\u0442\u0441\u044f":8,"\u043f\u043e\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0435\u0442":8,"\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0430\u0435\u0442\u0441\u044f":7,"\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0430\u0442\u044c\u0441\u044f":1,"\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f":[1,7],"\u043f\u043e\u0434\u0441\u0438\u0441\u0442\u0435\u043c\u0443":0,"\u043f\u043e\u043b\u0435":[0,2],"\u043f\u043e\u043b\u0443\u0447\u0430\u0435\u0442":[0,7],"\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c":0,"\u043f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044f":7,"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u0435":9,"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f":[2,9],"\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b":2,"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439":[0,7],"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u043c":[0,1],"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c":[0,7],"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044e":0,"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f":[0,1,7],"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c":1,"\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f\u043c\u0438":0,"\u043f\u043e\u043b\u044f":0,"\u043f\u043e\u043c\u043e\u0449\u044c\u044e":1,"\u043f\u043e\u0440\u0442":[1,7,8],"\u043f\u043e\u0440\u0442\u0430":[2,7,9],"\u043f\u043e\u0440\u0442\u0435\u0436\u0435\u0439":7,"\u043f\u043e\u0440\u0442\u0443":8,"\u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e":7,"\u043f\u043e\u0441\u0442\u0443\u043f\u0430\u0435\u043c\u044b\u0445":0,"\u043f\u043e\u0442\u0435\u0440\u0438":0,"\u043f\u043e\u0442\u043e\u043a\u0430":0,"\u043f\u043e\u0442\u0443\u0440\u044f":2,"\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c":7,"\u043f\u0440\u0435\u0440\u0432\u0430\u043b\u0430\u0441\u044c":7,"\u043f\u0440\u0438":[0,7,8,9],"\u043f\u0440\u0438\u0435\u043c\u0430":[0,9],"\u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435":[0,1],"\u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f":[0,1,2,7],"\u043f\u0440\u0438\u043c\u0435\u0440\u044b":[1,8],"\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u0435\u0442":7,"\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u044e\u0442\u0441\u044f":[1,8],"\u043f\u0440\u0438\u043d\u0438\u043c\u0430\u044e\u0449\u0435\u0433\u043e":8,"\u043f\u0440\u0438\u043d\u044f\u0442\u043e\u043c":2,"\u043f\u0440\u0438\u043d\u044f\u0442\u044b\u0445":7,"\u043f\u0440\u0438\u0441\u0443\u0442\u0441\u0442\u0432\u0438\u0438":0,"\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430":9,"\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438":[0,2],"\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0443":0,"\u043f\u0440\u043e\u0432\u0435\u0440\u044f\u0435\u0442":[2,7],"\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430":[1,8],"\u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b":7,"\u043f\u0440\u043e\u0435\u043a\u0442\u0430":2,"\u043f\u0440\u043e\u0438\u0437\u043e\u0439\u0434\u0451\u0442":1,"\u043f\u0443\u0431\u043b\u0438\u0447\u043d\u044b\u0435":8,"\u043f\u0443\u0431\u043b\u0438\u0447\u043d\u044b\u0439":[0,7],"\u043f\u0443\u0441\u0442\u043e\u0435":0,"\u0440\u0430\u0431\u043e\u0442\u0443":0,"\u0440\u0430\u0431\u043e\u0442\u044b":8,"\u0440\u0430\u0437\u0431\u0438\u0440\u0430\u0435\u0442":0,"\u0440\u0430\u0437\u043d\u0438\u0446\u0435\u0439":0,"\u0440\u0435\u0430\u043b\u0438\u0437\u0443\u0435\u0442":[0,7],"\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438":7,"\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f":7,"\u0440\u0435\u0436\u0438\u043c\u0435":8,"\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442":0,"\u0441":[0,1,2,7,8,9],"\u0441\u0432\u044f\u0437\u0438":2,"\u0441\u0432\u044f\u0437\u044c":7,"\u0441\u0435\u0440\u0432\u0435\u0440":[0,2,8],"\u0441\u0435\u0440\u0432\u0435\u0440\u0430":[0,1,2,6,7,8,9],"\u0441\u0435\u0440\u0432\u0435\u0440\u0435":[2,7],"\u0441\u0435\u0440\u0432\u0435\u0440\u043d\u044b\u0439":8,"\u0441\u0435\u0440\u0432\u0435\u0440\u043e\u043c":0,"\u0441\u0435\u0440\u0432\u0435\u0440\u0443":[0,1],"\u0441\u0435\u0442\u0438":1,"\u0441\u0438\u0433\u043d\u0430\u043b\u043e\u0432":0,"\u0441\u0438\u0441\u0442\u0435\u043c\u0443":1,"\u0441\u043b\u043e\u0432\u0430\u0440\u0435":[2,9],"\u0441\u043b\u043e\u0432\u0430\u0440\u0435\u043c":2,"\u0441\u043b\u043e\u0432\u0430\u0440\u0438":8,"\u0441\u043b\u043e\u0432\u0430\u0440\u044f":7,"\u0441\u043b\u043e\u0442":0,"\u0441\u043b\u043e\u0442\u0430\u043c\u0438":0,"\u0441\u043b\u0443\u0447\u0430\u044f":2,"\u0441\u043e":[0,7],"\u0441\u043e\u0431\u0435\u0441\u0435\u0434\u043d\u0438\u043a\u0430":0,"\u0441\u043e\u0434\u0435\u0440\u0436\u0430\u0449\u0438\u0439":0,"\u0441\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u0435":0,"\u0441\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u044f":[0,7,8],"\u0441\u043e\u0437\u0434\u0430\u0435\u0442":[0,7],"\u0441\u043e\u043a\u0435\u0442":[7,9],"\u0441\u043e\u043a\u0435\u0442\u0430":[2,9],"\u0441\u043e\u043e\u0431\u0449\u0430\u0435\u0442":0,"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435":[0,7,9],"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0439":[0,1,7,8,9],"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f":[0,1,7,8,9],"\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f\u043c\u0438":1,"\u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435":0,"\u0441\u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442":[0,7,9],"\u0441\u043f\u0438\u0441\u043a\u0430":0,"\u0441\u043f\u0438\u0441\u043a\u0435":2,"\u0441\u043f\u0438\u0441\u043e\u043a":[0,7],"\u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0438":7,"\u0441\u0442\u0430\u0440\u0442\u043e\u0432\u044b\u0439":0,"\u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0438":7,"\u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u043e\u0439":7,"\u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0443":7,"\u0441\u0442\u0438\u043b\u044c":8,"\u0441\u0442\u043e\u0440\u043e\u043a\u0438":8,"\u0441\u0442\u0440\u043e\u043a\u0438":[1,9],"\u0441\u0443\u0449\u0435\u0441\u0442\u0432\u043e\u0432\u0430\u043d\u0438\u0435":7,"\u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442":[0,7],"\u0442\u0430\u0431\u043b\u0438\u0446\u0435":[0,7],"\u0442\u0430\u0431\u043b\u0438\u0446\u0443":[0,7],"\u0442\u0430\u0431\u043b\u0438\u0446\u044b":[0,7],"\u0442\u0435\u043a\u0441\u0442":0,"\u0442\u0435\u0441\u0442":9,"\u0442\u0435\u0441\u0442\u043e\u0432":9,"\u0442\u0435\u0441\u0442\u043e\u0432\u0430\u044f":9,"\u0442\u0435\u0441\u0442\u044b":9,"\u0442\u0438\u043f\u0430":9,"\u0442\u043e":[2,7,9],"\u0442\u043e\u043b\u044c\u043a\u043e":8,"\u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u0430":0,"\u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u043d\u043e\u0433\u043e":0,"\u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u043d\u0443\u044e":0,"\u0443":7,"\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435":[0,7],"\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f":[0,7],"\u0443\u0434\u0430\u043b\u044f\u0435\u043c\u043e\u0433\u043e":7,"\u0443\u0434\u0430\u043b\u044f\u0435\u043c\u044b\u0439":0,"\u0443\u0434\u0430\u043b\u044f\u0435\u0442":[0,7],"\u0443\u0436\u0435":0,"\u0443\u043a\u0430\u0437\u0430\u043d\u0438\u0435\u043c":1,"\u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e":[1,9],"\u0443\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442":0,"\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0443":9,"\u0443\u0442\u0438\u043b\u0438\u0442":9,"\u0444\u0430\u043a\u0442":7,"\u0444\u0438\u043a\u0441\u0438\u0440\u0443\u0435\u0442":7,"\u0444\u0438\u043a\u0441\u0438\u0440\u0443\u044e\u0449\u0438\u0439":2,"\u0444\u043b\u0430\u0433":0,"\u0444\u043e\u0440\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435":[0,7],"\u0444\u043e\u0440\u043c\u0438\u0440\u0443\u0435\u0442":[0,7],"\u0444\u0443\u043d\u043a\u0446\u0438\u0438":[2,9],"\u0444\u0443\u043d\u043a\u0446\u0438\u0439":8,"\u0444\u0443\u043d\u043a\u0446\u0438\u044f":[0,2,8,9],"\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u0435":7,"\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f":0,"\u0445\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435":[0,7],"\u0445\u0440\u0430\u043d\u0438\u0442":8,"\u0445\u0440\u0430\u043d\u044f\u0449\u0443\u044e":0,"\u0445\u044d\u0448":7,"\u0446\u0438\u043a\u043b":[0,7],"\u0447\u0442\u043e":[2,9],"\u0448\u0438\u0444\u0440\u043e\u0432\u0430\u043d\u0438\u044f":0,"\u0448\u0438\u0444\u0440\u0443\u044e\u0442\u0441\u044f":1,"\u044d\u043a\u0437\u0435\u043c\u043f\u043b\u044f\u0440":[0,8],"\u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f":2,"\u044f\u0432\u043b\u044f\u044e\u0442\u0441\u044f":1,"case":9,"class":[0,2,7,9],"do":5,"new":[0,7],"return":[0,2,7,8,9],"true":7,It:5,The:[0,7],_config:8,_contact:0,_databas:8,_server:8,accept:[0,7],account_nam:9,action:9,active_users_list:7,activeus:7,add_contact:[0,7],add_contact_act:0,add_contact_window:0,add_us:[0,7],addcontactdialog:0,address:0,all_users_fil:7,allus:7,ani:[0,7],argument:[0,7],attribut:[0,7],automodul:[],bad:9,base:[0,2,7,9],bit:1,call:[0,7],cannot:[0,7],check_contact:0,check_us:[0,7],click:0,client:[1,3,5,7],client_app:3,client_db:3,client_log_config:3,clientdb:0,clientmainwindow:0,clientmak:2,clients_list_upd:0,clienttransport:0,close:5,clsdict:2,clsname:2,com:5,common:3,config:7,configwindow:7,connection_init:0,connection_lost:0,contact:[0,7],contacts_clear:0,contacts_list_request:0,create_pres:0,create_stat_model:7,create_users_model:7,databas:[0,7],date:0,decl_api:[0,7],deco:3,del_contact:0,delcontactdialog:0,delete_contact:0,delete_contact_window:0,deleteuserdialog:7,descrptr:3,dialog_add_contact:3,dialog_add_us:3,dialog_config:3,dialog_del_contact:3,dialog_remove_us:3,dialog_start:3,direct:0,error:[3,9],error_dict:9,except:2,exit:8,fals:7,featureless:[0,7],file_with_arg:5,func:2,get_contact:[0,7],get_histori:0,get_password:7,get_public_kei:7,get_subprocess:5,get_us:0,given:[0,7],guest:9,gui:8,ha:[0,7],hierarchi:[0,7],history_list_upd:0,http:5,id:[0,7],incorrectdatareceivederror:2,index:3,inform:5,inherit:[],init_socket:7,init_ui:7,instanc:[0,7],ip:7,ip_address:7,item:0,kei:0,key_request:0,kill:5,knownus:0,kwarg:[0,7],last_conn:7,launcher:[3,5],launcher_ubuntu:3,listen:5,listen_address:7,listen_port:7,localhost:8,log:[2,3],login:7,login_requir:2,loginhistori:7,main:8,main_window:3,main_window_ui:3,mainclientwindow:0,mainwindow:7,make_connect:0,max_len:9,member:[],messag:[0,7],message_205:0,message_statist:7,message_to_send:9,messagehistori:0,metaclass:3,metadata:[0,7],methodnam:9,missing_field:2,missingcli:2,modul:3,more:5,n:[1,8],name:[0,1],new_contact:0,new_messag:0,no_gui:8,nondictinputerror:2,none:[0,2,7,8],object:[0,2,7,9],open_file_dialog:7,orm:[0,7],out:0,p:[1,8],packag:3,page:3,param:2,paramet:[0,2,7,8,9],pass_hash:7,password:[0,1,7],path:7,port:[0,2,7],possible_contacts_upd:0,presenc:9,process:5,process_answ:0,process_client_messag:7,process_messag:7,pub_kei:0,pubkei:7,public_kei:7,py:[1,8],pyqt5:[0,7],python:[1,8],qdialog:[0,7],qmainwindow:[0,7],qmodel:7,qobject:0,qtcore:0,qtwidget:[0,7],question:5,receiv:7,recipi:[0,7],recv:9,register_us:7,registerus:7,registri:[0,7],remove_cli:7,remove_contact:[0,7],remove_us:7,reqfieldmissingerror:2,request:9,respons:9,retranslateui:0,rsa:1,run:[0,7],runtest:9,save_data:7,save_messag:0,save_server_config:7,search:3,select_active_us:0,send:9,send_messag:0,sender:[5,7],sent:7,server:[3,5,8],server_app:3,server_config:7,server_cor:3,server_db:3,server_log_config:3,serverdb:7,servererror:2,servermak:2,service_update_list:7,set_active_us:0,set_disabled_input:0,setupui:0,show:[],show_statist:7,signal_205:0,sock:7,sqlalchemi:[0,7],stackoverflow:5,start:5,start_server_gui:8,stat_window:3,statisticwindow:7,submodul:3,subprocess:5,success_dict:9,termin:5,test1:1,test_client:3,test_dict:9,test_dict_send:9,test_get_message_err:9,test_get_message_ok:9,test_get_tcp_parameters_address:9,test_get_tcp_parameters_default_address:9,test_get_tcp_parameters_default_port:9,test_get_tcp_parameters_default_server_address:9,test_get_tcp_parameters_port:9,test_get_tcp_parameters_returned_typ:9,test_send_messag:9,test_send_message_rais:9,test_serv:3,test_util:3,testcas:9,testsocket:9,testutil:9,text:2,thread:[0,7],time:9,time_conn:7,trans_obj:0,transport:3,transport_shutdown:0,two:5,type:[2,5],typeerror:2,ui_mainclientwindow:0,undoc:[],unit_test:3,unittest:9,update_possible_us:0,user:[0,7,9],user_author:7,user_list_request:0,user_login:7,user_login_histori:7,user_logout:7,usernam:[0,7],usernamedialog:0,users_list:[0,7],userscontact:7,usersmessagestat:7,util:3,variabl:3,when:[0,7],window:[4,5]},titles:["client package","client_app module","common package","Welcome to BelMessenger Project\u2019s documentation!","launcher module","launcher_ubuntu module","log package","server package","server_app module","unit_tests package"],titleterms:{belmesseng:3,client:0,client_app:1,client_db:0,client_log_config:6,common:2,content:[0,2,3,6,7,9],deco:2,descrptr:2,dialog_add_contact:0,dialog_add_us:7,dialog_config:7,dialog_del_contact:0,dialog_remove_us:7,dialog_start:0,document:3,error:2,indic:3,launcher:4,launcher_ubuntu:5,log:6,main_window:[0,7],main_window_ui:0,metaclass:2,modul:[0,1,2,4,5,6,7,8,9],packag:[0,2,6,7,9],project:3,s:3,server:7,server_app:8,server_cor:7,server_db:7,server_log_config:6,stat_window:7,submodul:[0,2,6,7,9],tabl:3,test_client:9,test_serv:9,test_util:9,transport:0,unit_test:9,util:2,variabl:2,welcom:3}})