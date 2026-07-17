from Modelos.Cuentas.client import Client
from Modelos.Roles.administrative import Administrative
from Modelos.Roles.analist import Analist
from Modelos.Roles.director import Director
from Modelos.Roles.logistic import Logistic
from Servicios.bank import Bank
from Servicios.bonus_admin import BonusAdmin

if __name__ == "__main__":
    bonus_admin = BonusAdmin()
    
    bank = Bank("DataBank", 2980374, clients = [], employees = [], global_transactions= [], logs=[], bonus_admin= bonus_admin)
    
    dir_caro = Director("Carolina", 63947527, "Humanas", 3, "julilaura")
    bank.employees.append(dir_caro)
    new_e = Analist("Diego", 1011232219, 2, "julyalejo")
    e_2= Administrative("Laura", 1021678463, 5, "julilaura21.")
    e_3= Logistic("Efi", 52541022, 10, "julyalejo")

    #VERIFICACION DE MANAGE EMPLOYEES

    #Verificacion de añadir empleados
    bank.manage_employees.add_employee(dir_caro, new_e)
    bank.manage_employees.add_employee(dir_caro, e_2)
    bank.manage_employees.add_employee(dir_caro, e_3)

    #Verificar que cambie los roles
    new_e = bank.manage_employees.change_role(dir_caro, new_e, "Administrativo", "Humanas")
    print (type(new_e).__name__)

    #Verificar update_experience
    print (e_2.experience)
    bank.manage_employees.update_experience(e_2, 15)
    print(e_2.experience)

    #Verificar eliminar employee
    bank.manage_employees.delete_employee(dir_caro, e_3)

    #VERIFICAR MANAGE ACCOUNTS
    cliente = Client("Juan", 1011232219, 25, "Ingeniero")
    bank.clients.append(cliente)

    #Creación de cuentas
    cuenta = bank.manage_accounts.create_account(dir_caro, cliente, "Ahorros")
    print(type(cuenta).__name__)
    print(cuenta)

    cliente_2 = Client("Prisci", 41560746, 75, "Pensionada")
    bank.clients.append(cliente_2)

    #Creación y activación de una cuenta
    cuenta_2 = bank.manage_accounts.create_account(dir_caro, cliente_2, "Corriente")
    cuenta_2.deposit(50000)
    fee = cuenta_2.get_balance() * 0.03

    cliente_3 = Client("Grillo", 75416258, 19, "Estudiante")
    bank.clients.append(cliente_3)

    cuenta_3 = bank.manage_accounts.create_account(dir_caro, cliente_3, "Juvenil")

    cliente_4 = Client("Nore", 95624785, 80, "Pensionada")
    bank.clients.append(cliente_4)

    cuenta_4 = bank.manage_accounts.create_account(dir_caro, cliente_4, "Ahorros")

    #Eliminar cuentas
    bank.manage_accounts.delete_account(dir_caro, cuenta)

    #Aplicar cargos
    bank.manage_accounts.apply_monthly_fee(dir_caro, cuenta_2, fee)
    print(cuenta_2.get_balance())

    #MANAGE CREDITS
    req_credit_1 = bank.manage_credits.request_credit(cliente_2, 20000, 10)
    req_credit_2 = bank.manage_credits.request_credit(cliente_4, 5000, 53)

    bank.manage_credits.approve_credit(dir_caro, cliente_2, req_credit_1)
    bank.manage_credits.reject_credit(cliente_4, req_credit_2)

    print(bank.manage_credits.calculate_credit_interest(req_credit_1))
    print (f"La cuota del crédito es de: {bank.manage_credits.calculate_monthly_installment(req_credit_1)}")

    #MANAGE CARDS
    card = bank.manage_cards.create_card(cuenta_2, "2109", False, True)
    card_2 = bank.manage_cards.create_card(cuenta_3, "5342", True, False)

    #bloqueo y debloqueo de tarjeta
    bank.manage_cards.block_card(card)
    bank.manage_cards.unblock_card(card)

    #cambio de pin
    bank.manage_cards.change_card_pin(card, "2109", "2804")

    #LIST OBJECTS
    for account in bank.list_objects.list_accounts(dir_caro):
        print (account)
    for account in bank.list_objects.list_employees(dir_caro):
        print (account)
    for account in bank.list_objects.list_active_credits():
        print (account)
    for account in bank.list_objects.list_cards():
        print (account)
    for account in bank.list_objects.list_cards_by_client(cliente_2):
        print (account)
    for account in bank.list_objects.list_accounts_by_client(cliente_2):
        print (account)

    #ANALIZE
    print (bank.analize.get_total_bank_money())
    print("Transacciones totales:")
    print (bank.analize.get_total_transactions())
    print("Operaciones sospechosas:")
    print (bank.analize.detect_suspicious_operations())
    print("Tipo de cuenta mas usada:")
    print (bank.analize.get_most_used_account_type())
    print("Top clientes")
    for client in bank.analize.get_top_clients(3):
        print (client)
    print("Clasificar cliente")
    print (bank.analize.classify_client(cliente_2))
    print("Calcular score:")
    print (bank.analize.calculate_client_score(cliente_2))

    #AUTENTICATE
    print(bank.autenticate.autenticate_user(dir_caro, "julilaura"))   
    print(bank.autenticate.autenticate_user(dir_caro, "wrongpass"))   
    print(bank.autenticate.autenticate_user(dir_caro, "wrongpass"))   
    print(bank.autenticate.autenticate_user(dir_caro, "wrongpass"))   
    print(dir_caro.is_blocked)                                        
    bank.autenticate.unblock_employee(dir_caro)
    print(dir_caro.is_blocked)                                        
    print(dir_caro.failed_attempts)  

    #NOTIFICATE
    bank.notificate.send_notification("client", "Su cuenta ha sido actualizada.")
    bank.notificate.send_notification("employee", "Reunión a las 3pm.")
    bank.notificate.notify_account_blocked()

    #REPORT
    print(bank.report.generate_employee_report())
    bank.report.generate_security_report()
    print(bank.report.generate_credit_report())
    print(bank.report.generate_clients_report())
    print(bank.report.generate_accounts_report())
    print(bank.report.generate_financial_report())

    #SEARCH
    print("\n SEARCH")
    print(bank.search.search_client_by_dni(41560746))     
    print(bank.search.search_client_by_dni(99999999))     
    print(bank.search.search_client_by_name("Grillo"))    
    print(bank.search.search_employee_by_dni(63947527))   
    print(bank.search.search_employee_by_name("Laura"))   

    for account in bank.search.search_account_by_bank(2980374):
        print (account)    
    for log in bank.search.employee_activity_history(dir_caro):
        print (log)

    # TRANSFER ENTRE CUENTAS
    cuenta_2.deposit(100000)
    cuenta_2.transfer(30000, cuenta_3)
    print(f"Saldo cuenta_2 tras transferencia: {cuenta_2.get_balance()}")
    print(f"Saldo cuenta_3 tras transferencia: {cuenta_3.get_balance()}")

    # BLOQUEO TEMPORAL
    bank.temporary_account_lock(cuenta_3, 1)
    print(f"Cuenta_3 bloqueada hasta: {cuenta_3.locked_until}")
    try:
        cuenta_3.deposit(1000)
    except Exception as e:
        print(f"Error esperado: {e}")

    # SORT ACCOUNTS
    print("Cuentas por número:")
    for acc in bank.sort_accounts_by_number():
        print(acc)
    print("Cuentas por saldo:")
    for acc in bank.sort_accounts_by_balance():
        print(acc)

    # EXPORT JSON
    bank.export_data_json()
    print("JSON exportado correctamente")

    # BLACKLIST CLIENT
    bank.blacklist_client(dir_caro, cliente_3, "Actividad sospechosa")
    print(f"{cliente_3.name} en lista negra: {cliente_3.is_blacklisted}")
    print(f"Motivo: {cliente_3.blacklist_reason}")

    # BONUS
    bank.register_global_bonus()
    print(f"Bonus total: {bank.get_total_bonus()}")

    # PAY CREDIT INSTALLMENT
    cuota = bank.manage_credits.calculate_monthly_installment(req_credit_1)
    for i in range(10):
        banco_restante = bank.manage_credits.pay_credit_installment(cliente_2, req_credit_1, cuota)
        print(f"Cuota {i+1} pagada. Saldo restante: {banco_restante}")
    print(f"Estado del crédito: {req_credit_1.status}")

    # SALARY
    print(f"Salario e_2 antes: {e_2.get_salary()}")
    bank.manage_employees.approve_salary_increase(dir_caro, e_2, 2000)
    print(f"Salario e_2 tras aumento manual: {e_2.get_salary()}")
    bank.manage_employees.apply_salary_increase(dir_caro, e_2)
    print(f"Salario e_2 tras aumento porcentual: {e_2.get_salary()}")