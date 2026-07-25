import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime, timedelta
from Servicios.bank import Bank
from Servicios.bonus_admin import BonusAdmin
from Modelos.Cuentas.client import Client
from Modelos.Roles.director import Director
from Modelos.Roles.administrative import Administrative
from Modelos.Roles.analist import Analist
from Modelos.Roles.logistic import Logistic
from Servicios.auditlog import AuditLog
from Servicios.promotion_request import PromotionRequest
from Servicios.salary_inc_req import SalaryIncreaseRequest


bonus_admin = BonusAdmin()
global bank
bank = Bank("DataBank", 2980374, clients = [], employees = [], global_transactions= [], logs=[], bonus_admin= bonus_admin)

# Se carga todo lo que ya se había guardado en corridas anteriores ANTES de crear
# cualquier dato nuevo, para que la información vieja no se pierda.
bank.import_data_json()

# La directora por defecto solo se crea la primera vez
if bank.search.search_employee_by_dni(1021678463) is None:
    director = Director("Laura Espinosa", 1021678463, "Ingeniería", 1, "julilaura")
    bank.employees.append(director)
else:
    director = bank.search.search_employee_by_dni(1021678463)

databank_app = tk.Tk()
palabra = tk.StringVar(databank_app) #guardar strings y se mapea a algun lugar de la app
entrada = tk.StringVar(databank_app)

#dimensiones: Anchura por Altura
databank_app.geometry("600x600") 
databank_app.configure(background="#00296b")
#Se pone titulo con el windows manager
tk.Wm.wm_title(databank_app, "DataBank")

global account_types
account_types = ["Ahorros", "Corriente", "Empresarial", "Juvenil"]

def clean_screen():
    for widget in databank_app.winfo_children(): #winfo childern devuelve una lista con todos los widgets hijos de una ventana
        widget.destroy()

def go_to_main_screen():
    clean_screen()

    welcome_title = tk.Label(
        databank_app,
        text="Bienvenido a DataBank",
        font=("Courier", 24, "bold"),
        fg="white",
        bg="#00296b"
    )
    welcome_title.pack(
        fill= tk.BOTH,
        pady=(300, 50)
    )
    
    marker_text = "Ingrese su nombre..."

    data_entry = tk.Entry(
        databank_app,
        fg="gray",
        bg="black",
        font=("Courier", 14),
        justify="center",
        relief="flat"
    )
    data_entry.pack(pady=20, ipady=5)
    data_entry.insert(0, marker_text)

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=5)

    def into_the_entry (event):
        if data_entry.get() == marker_text: #ejecutar al hacer clic o entrar al campo
            data_entry.delete(0, tk.END) #borra el marcador
            data_entry.config(fg="white") #para simular ello, cambia el texto a blanco

    def out_the_entry(event):
        if data_entry.get() == "":
            data_entry.insert(0, marker_text)
            data_entry.config(fg="gray") #por si se sale, vuelve a aparecer el texto

    #se enlazan los eventos al entry
    data_entry.bind("<FocusIn>", into_the_entry) #detecta cuando se hace clic sobre el cuadro
    data_entry.bind("<FocusOut>", out_the_entry) #detecta cuando se hace clic fuera del cuadro

    def validate_and_continue():
        name = data_entry.get().strip()

        if name == "" or name == marker_text:
            label_error.config(text="Por favor, escribe un nombre válido.")
        else:
            go_to_main_menu(name)

    tk.Button(
        databank_app,
        text="Continuar",
        font=("Courier", 14, "bold"),
        bg="white",
        fg="#00296b",
        command=validate_and_continue, # Llama a la validación
        relief="flat",
        activebackground="#9C9C9C",  
        activeforeground="white"
    ).pack(pady=20, ipadx=15, ipady=7)

def go_to_main_menu(username):
    clean_screen()

    #cargar las imagenes
    global client_img, employee_img #para que la variable sea global, no sólo cuando se ejecute la función
    client_img_1 = tk.PhotoImage(file="client.png")
    employee_img_2 = tk.PhotoImage(file="employee.png")

    client_img = client_img_1.subsample(2, 2)   # Reduce a la mitad
    employee_img = employee_img_2.subsample(2, 2)

    system_title= tk.Label(
        databank_app,
        text=f"¡Hola, {username}!\nSelecciona el rol que ocupas:",
        font=("Courier", 24, "bold"),
        fg="white",
        bg="#00296b"
    )
    system_title.pack(pady=(80,50))

    button_container = tk.Frame(
        databank_app,
        bg = "#00296b"
    )

    button_container.pack(pady=20) #esta es la separación con el título

    tk.Button(
        button_container,
        text= "Cliente",
        image= client_img,
        compound="top", #se pone la imagen encima del texto
        font=("Courier", 16, "bold"),
        bg= "#00296b",
        fg= "white",
        relief="flat",
        activebackground= "#9C9C9C",
        activeforeground= "white",
        command= lambda: process_client_selection(username, bank)
    ).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=8)

    tk.Button(
        button_container,
        text= "Empleado",
        image= employee_img,
        compound="top",
        font=("Courier", 16, "bold"),
        bg= "#00296b",
        fg= "white",
        relief="flat",
        activebackground= "#9C9C9C",
        activeforeground= "white",
        command = lambda : go_to_employee_login_screen(username,bank)
    ).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=8)

    tk.Button(
        databank_app,
        text="Cerrar Sesión",
        font=("Courier", 12),
        bg="#d9534f",
        fg="white",
        relief="flat",
        command=go_to_main_screen
    ).pack(pady=(80, 0), ipadx=10, ipady=5)

databank_title = tk.Label( #widget que contiene texto
    databank_app,
    text= "DataBank",
    font = ("Courier", 45, "bold"),
    fg= "white",
    bg="#00296b",
    justify= "center",
    relief="flat"
)
databank_title.pack(
    fill= tk.BOTH,
    pady=(300, 50)
) 

tk.Button(
    databank_app, #donde queremos incrustar
    text="Click para ingresar",
    font=("Courier", 14),
    bg = "white",
    fg="#00296b",
    command= go_to_main_screen,
    relief="flat",
    activebackground="#9C9C9C",  
    activeforeground="white"
).pack(
    pady=(10),
    ipadx= 10,
    ipady= 7   
    # sin expand=True, así el botón tiene tamaño preferido
) #Pack incrusta y empaqueta el boton dentro de nuestra aplicacion


def go_to_register_client_screen(username, bank):
    clean_screen()

    tk.Label(
        databank_app,
        text="¡Gracias por querer ser parte de DataBank!",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=30)

    # Mostramos el nombre que ya ingresó en la primera pantalla (fijo, no editable)
    tk.Label(
        databank_app, 
        text=f"Nombre de usuario elegido: {username}", 
        font=("Courier", 12, "italic"), 
        fg="yellow", 
        bg="#00296b"
    ).pack(pady=10)

    tk.Label(
        databank_app, 
        text="Número de DNI o Cédula:", 
        font=("Courier", 12), fg="white", 
        bg="#00296b"
    ).pack(pady=5)

    entry_dni = tk.Entry(
        databank_app, 
        font=("Courier", 12), 
        justify="center"
    )
    entry_dni.pack(pady=5)

    tk.Label(
        databank_app, 
        text="Edad:", 
        font=("Courier", 12), 
        fg="white", 
        bg="#00296b").pack(pady=5)
    entry_age = tk.Entry(
        databank_app, 
        font=("Courier", 12), 
        justify="center"
    )
    entry_age.pack(pady=5)

    tk.Label(
        databank_app, 
        text="Ocupación o Profesión:", 
        font=("Courier", 12), 
        fg="white", 
        bg="#00296b"
    ).pack(pady=5)
    entry_occupation = tk.Entry(
        databank_app, 
        font=("Courier", 12), 
        justify="center"
    )
    entry_occupation.pack(pady=5)


    data_auth_var = tk.IntVar(value=0) # 0 = Desmarcado, 1 = Marcado
    
    auth_checkbox = tk.Checkbutton(
        databank_app,
        text="Autorizo el tratamiento de mis datos personales\ncon tal de hacer funcionar este proyecto",
        variable=data_auth_var,
        onvalue=1,
        offvalue=0, #fuerza a que cuando se desmarque vuelva a valer 0 la checkbox
        font=("Courier", 10),
        fg="white",
        bg="#00296b",
        activebackground="#00296b",
        activeforeground="white",
        selectcolor="#00183f", # Color de fondo del cuadrito interno cuando se marca
        justify="center"
    )
    auth_checkbox.pack(pady=15)

    auth_checkbox.variable = data_auth_var

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=5)

    def save_new_client():
        dni_text = entry_dni.get().strip()
        age_text = entry_age.get().strip()
        occupation = entry_occupation.get().strip()
    
        if not dni_text or not age_text or not occupation:
            label_error.config(text="Todos los campos son obligatorios. Asegúrese de que no falte alguno.")
            return
        
        if auth_checkbox.variable.get() == 0:
            label_error.config(text="Debe autorizar el tratamiento de datos para continuar.")
            return

        try:
            dni = int(dni_text)
            age = int(age_text)

            new_client = Client(name=username, dni=dni, age=age, profession=occupation)
            new_client.registration_date = datetime.now()
            bank.clients.append(new_client)
            
            print(f"Nuevo objeto Client guardado en el backend para {username}.")

            go_to_client_operations(new_client, bank)

        except ValueError:
            label_error.config(text="DNI y Edad deben ser números válidos.")

    tk.Button(
        databank_app,
        text="Finalizar Registro",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        command=save_new_client,
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white"
    ).pack(pady=20, ipadx=10, ipady=5)

def process_client_selection(username, bank):
    client_found = bank.search.search_client_by_name(username)

    if client_found and not isinstance(client_found, str):
        print(f"Cliente encontrado: {client_found}. Redirigiendo...")
        go_to_client_operations(client_found, bank)
    else:
        print(f"El cliente -{username}- no existe. Espere un momento para ser registrado.")
        go_to_register_client_screen(username, bank)

def build_nav_bar(client_object, bank):
    is_menu_open = False

    sidebar_frame = tk.Frame(
        databank_app, 
        bg="#00183f", 
        width=200, 
        height=600
    )
    sidebar_frame.pack_propagate(False) #evita que cambie de tamaño
    sidebar_frame.place_forget() #para que inicie oculto

    tk.Label(
        sidebar_frame, 
        text="Menú", 
        font=("Courier", 14, "bold"), 
        fg="white", bg="#00183f"
    ).pack(pady=20, padx=10)
    
    menu_item_style = {"font": ("Courier", 11), "fg": "white", "bg": "#00183f", "relief": "flat", "anchor": "w"}
    
    tk.Button(
        sidebar_frame, 
        text="👤 Mis datos", #pongo el emoji porque así es más simple que poner mi propia imagen
        command=lambda: go_to_client_operations(client_object, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    tk.Button(
        sidebar_frame, 
        text="⚙️ Mi cuenta", 
        command=lambda: open_my_account_module(client_object, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    tk.Button(
        sidebar_frame, 
        text="🕒 Historial", 
        command=lambda: open_history_module(client_object, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    tk.Button(
        sidebar_frame, 
        text="📄 Mis solicitudes", 
        command=lambda: open_requests_module(client_object, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    #logica para alternar el menu
    def toggle_sidebar():
        nonlocal is_menu_open
        if not is_menu_open:
            top_bar_frame.update_idletasks()
            top_bar_height = top_bar_frame.winfo_height()


            sidebar_frame.place(x=0, y=top_bar_height, width=200, height=databank_app.winfo_height() - top_bar_height)
            sidebar_frame.lift() #trae el menu para que no quede oculto detrás del contenido
            menu_button.config(text="✕", bg="#00183f", fg="white") 
            is_menu_open = True
        else:
            sidebar_frame.place_forget()
            menu_button.config(text="☰", bg="#00296b", fg="white") 
            is_menu_open = False

    top_bar_frame = tk.Frame(
        databank_app, 
        bg="#00296b"
    )
    top_bar_frame.pack(fill="x", side="top", anchor="nw")

    menu_button = tk.Button(
        top_bar_frame,
        text="☰",
        font=("Courier", 18, "bold"),
        bg="#00296b",
        fg="white",
        relief="flat",
        activebackground="#00183f",
        activeforeground="white",
        command=toggle_sidebar
    )
    menu_button.pack(side="left", padx=10, pady=10)

    tk.Button(
        top_bar_frame,
        text="Cerrar Sesión",
        font=("Courier", 11),
        bg="#d9534f",
        fg="white",
        relief="flat",
        activebackground="#c9302c",
        activeforeground="white",
        command=lambda: go_to_main_screen(),
    ).pack(pady=20, ipadx=10, ipady=5, side="right")

    databank_label = tk.Label(
        top_bar_frame,
        text="DataBank",
        font=("Courier", 16, "bold"),
        fg="white",
        bg="#00296b",
    )
    databank_label.pack(side="right", padx=20, pady=10)
    databank_label.bind("<Button-1>", lambda event: go_to_client_operations(client_object, bank))

def go_to_client_operations(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    global card_img,account_img,credit_img,help_img
    card_img1 = tk.PhotoImage(file="card.png")
    account_img1 = tk.PhotoImage(file="account.png")
    credit_img1 = tk.PhotoImage(file="credit.png")
    help_img1 = tk.PhotoImage(file="help.png")

    card_img = card_img1.subsample(2,2)
    account_img = account_img1.subsample(2,2)
    credit_img = credit_img1.subsample(2,2)
    help_img = help_img1.subsample(2,2)


    tk.Label(
        databank_app,
        text=f"Panel del Cliente: {client_object.name}\nPerfil: {client_object.profession}",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") #anchor me ayuda a poner el texto hacia la izquierda

    frame_accounts = tk.LabelFrame(
        databank_app, 
        text=" Mis Productos ", 
        font=("Courier", 17, "bold"), 
        fg="white", 
        bg="#00296b", 
        padx=15, 
        pady=15
    )
    frame_accounts.pack(pady=10, padx=50, fill="x")

    accounts = bank.list_objects.list_accounts_by_client(client_object)
    if not accounts:
        tk.Label(frame_accounts, text="No tienes cuentas registradas.", font=("Courier", 16), fg="yellow", bg="#00296b").pack()
    else:
        for c in accounts:
            # type(c).__name__ dice si es corriente, ahorros o juvenil
            tk.Label(
                frame_accounts, 
                text=f"Cuenta {type(c).__name__} -> Saldo: ${c.get_balance()}", 
                font=("Courier", 11), 
                fg="white", 
                bg="#00296b"
            ).pack(anchor="w", pady=2)

    tk.Label(
        databank_app,
        text="Tus servicios:",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") #anchor me ayuda a poner el texto hacia la izquierda

    menu_operations = tk.Frame(databank_app, bg="#00296b")
    menu_operations.pack(pady=30)

    options_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white"
    }

    tk.Button(
        menu_operations,
        text="\nCuentas",
        command=lambda: open_account_module(client_object, bank),
        image=account_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nTarjetas",
        command=lambda: open_cards_module(client_object, bank),
        image=card_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nCréditos",
        command=lambda: open_credits_module(client_object, bank),
        image=credit_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAyuda",
        command=lambda: open_faq_module(client_object, bank),
        image=help_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

def open_account_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    accounts = bank.list_objects.list_accounts_by_client(client_object)

    if not accounts:
        tk.Label(
            content_frame, text="No tienes cuentas registradas.",
            font=("Courier", 16), fg="yellow", bg="#00296b"
        ).pack(anchor="w", pady=20)

        global selected_type_var, password_entry, error_label
        selected_type_var = tk.StringVar(value=account_types[0])

        creation_row = tk.Frame(content_frame, bg="#00296b")
        creation_row.pack(anchor="w", pady=15)

        tk.Label(
            creation_row, text="Tipo de cuenta a crear:",
            font=("Courier", 12), fg="white", bg="#00296b"
        ).pack(side="left", padx=(0, 10))

        type_menu = tk.OptionMenu(creation_row, selected_type_var, *account_types)
        type_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
        type_menu.pack(side="left")

        tk.Label(
            content_frame, text="Asigne una contraseña de 4 dígitos:",
            font=("Courier", 12), fg="white", bg="#00296b"
        ).pack(anchor="w", pady=(15, 5))

        password_entry = tk.Entry(content_frame, font=("Courier", 12), show="*", justify="left", width=15) #show="*" es para que no se muestre lo que se escribe
        password_entry.pack(anchor="w", pady=(0, 15), ipady=3)

        error_label = tk.Label(content_frame, text="", font=("Courier", 11), fg="red", bg="#00296b")
        error_label.pack(anchor="w", pady=5)

        def create_account_and_card_gui():
            selected_type = selected_type_var.get()
            password = password_entry.get().strip()

            if not password:
                error_label.config(text="La contraseña es obligatoria.")
                return
            if not password.isdigit() or len(password) != 4:
                error_label.config(text="La contraseña debe ser de exactamente 4 números.")
                return

            try:
                new_account = bank.manage_accounts.create_account(director, client_object, selected_type)
                if not new_account:
                    updated_accounts = bank.list_objects.list_accounts_by_client(client_object)
                    new_account = updated_accounts[-1]
                        
                is_credit = False
                is_debit = True
                
                new_card = bank.manage_cards.create_card(
                    account=new_account,
                    pin=password,
                    credit=is_credit,
                    debit=is_debit
                )

                if not hasattr(new_account, 'cards') or new_account.cards is None:
                    new_account.cards = []
                
                if new_card and new_card not in new_account.cards:
                    new_account.cards.append(new_card)

                show_thank_you_screen(client_object, bank)
            except ValueError as e:
                error_label.config(text=str(e))
            except Exception as e:
                error_label.config(text=f"Error en el proceso: {e}")

        tk.Button(
                content_frame,
                text="Crear cuenta y tarjeta",
                font=("Courier", 12, "bold"),
                bg="white",
                fg="#00296b",
                relief="flat",
                activebackground="#9C9C9C",
                activeforeground="white",
                command=create_account_and_card_gui
        ).pack(anchor="w", pady=15, ipadx=10, ipady=5)
        return

    def create_account_gui():
        selected_type = selected_type_var.get()
        password = password_entry.get().strip() if 'password_entry' in globals() or 'password_entry' in locals() else "1234"
        
        try:
            new_account = bank.manage_accounts.create_account(director, client_object, selected_type)
            if not new_account:
                updated_accounts = bank.list_objects.list_accounts_by_client(client_object)
                new_account = updated_accounts[-1]

            new_card = bank.manage_cards.create_card(
                account=new_account,
                pin=password,
                credit=False,
                debit=True
            )

            if not hasattr(new_account, 'cards') or new_account.cards is None:
                new_account.cards = []
            if new_card and new_card not in new_account.cards:
                new_account.cards.append(new_card)

            show_thank_you_screen(client_object, bank)
        except ValueError as e:
            error_label.config(text=str(e))
        except Exception as e:
            error_label.config(text=f"Error al crear la cuenta: {e}")

        tk.Button(
            content_frame,
            text="Crear cuenta",
            font=("Courier", 12, "bold"),
            bg="white",
            fg="#00296b",
            relief="flat",
            activebackground="#9C9C9C",
            activeforeground="white",
            command=create_account_gui
        ).pack(anchor="w", pady=10, ipadx=10, ipady=5)

        return

    selector_frame = tk.Frame(content_frame, bg="#00296b")
    selector_frame.pack(anchor="w", pady=(0, 20))

    tk.Label(
        selector_frame, text="Selecciona una cuenta:",
        font=("Courier", 13, "bold"), fg="white", bg="#00296b"
    ).pack(side="left", padx=(0, 10))

    def label_for(account):
        number = str(account.account_number)
        return f"{type(account).__name__} - ****{number[-4:]}"

    account_labels = [label_for(a) for a in accounts]
    selected_account_var = tk.StringVar(value=account_labels[0])

    def on_account_change(_):
        render_account_details()

    account_menu = tk.OptionMenu(selector_frame, selected_account_var, *account_labels, command=on_account_change)
    account_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    account_menu.pack(side="left")

    def open_creation_popup():
        popup = tk.Toplevel(databank_app)
        popup.title("Nueva Cuenta")
        popup.geometry("450x350")
        popup.configure(bg="#00296b")
        popup.resizable(False, False)
        popup.transient(databank_app)
        popup.grab_set()

        popup_frame = tk.Frame(popup, bg="#00296b", padx=30, pady=25)
        popup_frame.pack(fill="both", expand=True)

        tk.Label(
            popup_frame, text="Abrir Nueva Cuenta",
            font=("Courier", 14, "bold"), fg="yellow", bg="#00296b"
        ).pack(anchor="w", pady=(0, 15))

        popup_type_var = tk.StringVar(value=account_types[0])

        type_row = tk.Frame(popup_frame, bg="#00296b")
        type_row.pack(anchor="w", pady=10)

        tk.Label(
            type_row, text="Tipo:",
            font=("Courier", 12), fg="white", bg="#00296b"
        ).pack(side="left", padx=(0, 10))

        popup_menu = tk.OptionMenu(type_row, popup_type_var, *account_types)
        popup_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
        popup_menu.pack(side="left")

        tk.Label(
            popup_frame, text="Asigne contraseña de tarjeta (4 números):",
            font=("Courier", 11), fg="white", bg="#00296b"
        ).pack(anchor="w", pady=(15, 5))

        popup_password_entry = tk.Entry(popup_frame, font=("Courier", 12), show="*", justify="left", width=15)
        popup_password_entry.pack(anchor="w", pady=(0, 10), ipady=3)

        popup_error_label = tk.Label(popup_frame, text="", font=("Courier", 10), fg="red", bg="#00296b")
        popup_error_label.pack(anchor="w", pady=5)

        def execute_creation():
            selected_type = popup_type_var.get()
            password = popup_password_entry.get().strip()

            if not password:
                popup_error_label.config(text="La contraseña es obligatoria.")
                return
            if not password.isdigit() or len(password) != 4:
                popup_error_label.config(text="Debe tener exactamente 4 números.")
                return

            try:
                new_account = bank.manage_accounts.create_account(director, client_object, selected_type)
                if not new_account:
                    updated_accounts = bank.list_objects.list_accounts_by_client(client_object)
                    new_account = updated_accounts[-1]

                new_card = bank.manage_cards.create_card(
                    account=new_account,
                    pin=password,
                    credit=False,
                    debit=True
                )

                if not hasattr(new_account, 'cards') or new_account.cards is None:
                    new_account.cards = []
                if new_card and new_card not in new_account.cards:
                    new_account.cards.append(new_card)

                if not hasattr(client_object, 'requests_history'):
                    client_object.requests_history = []
                
                actual = datetime.now().strftime("%Y-%m-%d %H:%M")
                log = f"[{actual}] Creación de cuenta {selected_type} asignada con Tarjeta Débito."
                client_object.requests_history.append(log)
                
                popup.destroy()
                show_thank_you_screen(client_object, bank)

                popup.destroy() # se cierra la ventana emergente
                show_thank_you_screen(client_object, bank)
            except Exception as e:
                popup_error_label.config(text=f"Error: {e}")

        tk.Button(
            popup_frame,
            text="Crear cuenta",
            font=("Courier", 11, "bold"),
            bg="white", fg="#00296b",
            relief="flat",
            command=execute_creation
        ).pack(anchor="w", pady=15, ipadx=8, ipady=4)

    tk.Button(
        selector_frame, 
        text="➕ Crear cuenta", 
        command=open_creation_popup,
        font=("Courier", 11, "bold"), 
        bg="white", fg="#00296b", 
        relief="flat",
        activebackground="#9C9C9C", activeforeground="white"
    ).pack(side="left")

    details_frame = tk.Frame(content_frame, bg="#00296b")
    details_frame.pack(fill="x", anchor="w")

    balance_visible = {"value": False}
    account_visible = {"value": False}

    def get_selected_account():
        idx = account_labels.index(selected_account_var.get())
        return accounts[idx]

    def toggle_balance():
        balance_visible["value"] = not balance_visible["value"]
        render_account_details()

    def toggle_account_number():
        account_visible["value"] = not account_visible["value"]
        render_account_details()  

    def render_account_details():
        for widget in details_frame.winfo_children():
            widget.destroy()

        account = get_selected_account()
        number = str(account.account_number)

        account_row = tk.Frame(details_frame, bg="#00296b")
        account_row.pack(anchor="w", pady=5)
        
        if account_visible["value"]:
            account_text = f"No.Cuenta: {number}"
            account_btn_text = "Ocultar"
        else:
            account_text = f"No.Cuenta: ****{number[-4:]}"
            account_btn_text = "Click Para ver"

        tk.Label(
            account_row, 
            text=account_text,
            font=("Courier", 14, "bold"), 
            fg="white", 
            bg="#00296b"
        ).pack(anchor="w", padx=(0,15))

        tk.Button(
            account_row, 
            text=account_btn_text, 
            command=toggle_account_number,
            font=("Courier", 10, "bold"), 
            bg="white", fg="#00296b", 
            relief="flat"
        ).pack(side="left")

        balance_row = tk.Frame(details_frame, bg="#00296b")
        balance_row.pack(anchor="w", pady=5)

        if balance_visible["value"]:
            balance_text = f"Saldo: ${account.get_balance():,.2f}"
            button_text = "Ocultar"
        else:
            balance_text = "Saldo: ****"
            button_text = "Click para ver"

        tk.Label(
            balance_row, text=balance_text,
            font=("Courier", 14, "bold"), fg="white", bg="#00296b"
        ).pack(side="left", padx=(0, 15))

        tk.Button(
            balance_row, text=button_text, command=toggle_balance,
            font=("Courier", 10, "bold"), bg="white", fg="#00296b", relief="flat"
        ).pack(side="left")

        tk.Label(
            details_frame, text=f"Tipo: {type(account).__name__}",
            font=("Courier", 14, "bold"), fg="white", bg="#00296b"
        ).pack(anchor="w", pady=5)

        buttons_frame = tk.Frame(details_frame, bg="#00296b")
        buttons_frame.pack(fill="x", pady=25)

        operation_style = {
            "font": ("Courier", 13, "bold"), "bg": "white", "fg": "#00296b",
            "relief": "flat", "activebackground": "#9C9C9C", "activeforeground": "white"
        }

        tk.Button(
            buttons_frame, text="Transferir",
            command=lambda: open_transfer_module(account, client_object, bank),
            **operation_style
        ).pack(fill="x", pady=5, ipady=8)

        tk.Button(
            buttons_frame, text="Retirar",
            command=lambda: open_withdraw_module(account, client_object, bank),
            **operation_style
        ).pack(fill="x", pady=5, ipady=8)

        tk.Button(
            buttons_frame, text="Depositar",
            command=lambda: open_deposit_module(account, client_object, bank),
            **operation_style
        ).pack(fill="x", pady=5, ipady=8)

    render_account_details()

def show_thank_you_screen(client_object, bank):
    clean_screen()

    tk.Label(
        databank_app,
        text="¡Gracias!",
        font=("Courier", 26, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=(150, 20))

    tk.Label(
        databank_app,
        text="Tu cuenta ha sido creada exitosamente.\nVuelve al menú principal para continuar.",
        font=("Courier", 14),
        fg="white",
        bg="#00296b",
        justify="center"
    ).pack(pady=(0, 40))

    tk.Button(
        databank_app,
        text="Volver al panel",
        font=("Courier", 14, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=10, ipadx=15, ipady=7)

def open_transfer_module(account, client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    origin_number = str(account.account_number)

    tk.Label(
        content_frame,
        text=f"Transferir desde cuenta ****{origin_number[-4:]}",
        font=("Courier", 18, "bold"),
        fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 30))

    tk.Label(
        content_frame, text="Número de cuenta destino:",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 5))

    destination_entry = tk.Entry(content_frame, font=("Courier", 12), justify="left")
    destination_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    tk.Label(
        content_frame, text="Monto a transferir:",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 5))

    amount_entry = tk.Entry(content_frame, font=("Courier", 12), justify="left")
    amount_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    tk.Label(
        content_frame, text="Contraseña de la cuenta (4 dígitos):",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 5))

    password_entry = tk.Entry(content_frame, font=("Courier", 12), show="*", justify="left")
    password_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    error_label = tk.Label(content_frame, text="", font=("Courier", 11), fg="red", bg="#00296b")
    error_label.pack(anchor="w", pady=5)

    def transfer_gui():
        destination_text = destination_entry.get().strip()
        amount_text = amount_entry.get().strip()
        password_text = password_entry.get().strip()

        if not destination_text or not amount_text or not password_text:
            error_label.config(text="Todos los campos son obligatorios.")
            return

        try:
            destination_number = int(destination_text)
            amount = float(amount_text)
        except ValueError:
            error_label.config(text="El número de cuenta y el monto deben ser numéricos.")
            return

        if amount <= 0:
            error_label.config(text="El monto debe ser mayor a 0.")
            return

        if not account.cards:
            error_label.config(text="Esta cuenta no tiene una tarjeta asociada para validar.")
            return
        
        associated_card = account.cards[0] 
        
        if associated_card.get_pin() != password_text:
            error_label.config(text="Contraseña incorrecta. Operación cancelada.")
            return

        destination_account = bank.search.search_account_by_number(destination_number)

        if destination_account is None:
            error_label.config(text="La cuenta destino no existe.")
            return

        if destination_account.account_number == account.account_number:
            error_label.config(text="No puedes transferir a la misma cuenta.")
            return

        try:
            account.transfer(amount, destination_account)
            show_transfer_success_screen(client_object, bank)
        except Exception as e:
            error_label.config(text=f"Error al transferir: {e}")

    tk.Button(
        content_frame,
        text="Transferir",
        font=("Courier", 13, "bold"),
        bg="white", fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=transfer_gui
    ).pack(anchor="w", pady=10, ipadx=10, ipady=5)

def show_transfer_success_screen(client_object, bank):
    clean_screen()

    tk.Label(
        databank_app,
        text="¡Transferencia exitosa!",
        font=("Courier", 26, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=(150, 20))

    tk.Label(
        databank_app,
        text="Tu transferencia se realizó correctamente.",
        font=("Courier", 14),
        fg="white",
        bg="#00296b",
        justify="center"
    ).pack(pady=(0, 40))

    tk.Button(
        databank_app,
        text="Ver mis cuentas",
        font=("Courier", 14, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: open_account_module(client_object, bank)
    ).pack(pady=10, ipadx=15, ipady=7)

def open_withdraw_module(account, client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    number = str(account.account_number)
    tk.Label(content_frame, text=f"Retirar de cuenta ****{number[-4:]}", font=("Courier", 18, "bold"), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 30))

    tk.Label(content_frame, text="Monto a retirar:", font=("Courier", 12), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 5))
    amount_entry = tk.Entry(content_frame, font=("Courier", 12), justify="left")
    amount_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    tk.Label(
        content_frame, text="Contraseña de la cuenta (4 dígitos):",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 5))

    password_entry = tk.Entry(content_frame, font=("Courier", 12), show="*", justify="left")
    password_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    error_label = tk.Label(content_frame, text="", font=("Courier", 11), fg="red", bg="#00296b")
    error_label.pack(anchor="w", pady=5)

    def withdraw_gui():
        password_text = password_entry.get().strip()
        amount_text = amount_entry.get().strip()
        if not amount_text:
            error_label.config(text="Por favor, ingrese un monto.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            error_label.config(text="El monto debe ser un valor numérico.")
            return

        if amount <= 0:
            error_label.config(text="El monto debe ser mayor a 0.")
            return
        
        associated_card = account.cards[0] 
        
        if associated_card.get_pin() != password_text:
            error_label.config(text="Contraseña incorrecta. Operación cancelada.")
            return

        try:
            account.withdraw(amount) 
            show_success_screen(client_object, bank, "¡Retiro Exitoso!", "El dinero ha sido debitado de tu cuenta.")
        except Exception as e:
            error_label.config(text=f"Error: {e}")

    tk.Button(content_frame, text="Confirmar Retiro", font=("Courier", 13, "bold"), bg="white", fg="#00296b", relief="flat", command=withdraw_gui).pack(anchor="w", pady=10, ipadx=10, ipady=5)

def open_deposit_module(account, client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    number = str(account.account_number)
    tk.Label(content_frame, text=f"Depositar en cuenta ****{number[-4:]}", font=("Courier", 18, "bold"), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 30))

    tk.Label(content_frame, text="Monto a depositar:", font=("Courier", 12), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 5))
    amount_entry = tk.Entry(content_frame, font=("Courier", 12), justify="left")
    amount_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    tk.Label(
        content_frame, text="Contraseña de la cuenta (4 dígitos):",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 5))

    password_entry = tk.Entry(content_frame, font=("Courier", 12), show="*", justify="left")
    password_entry.pack(anchor="w", pady=(0, 20), ipady=5, fill="x")

    error_label = tk.Label(content_frame, text="", font=("Courier", 11), fg="red", bg="#00296b")
    error_label.pack(anchor="w", pady=5)

    def deposit_gui():
        password_text = password_entry.get().strip()
        amount_text = amount_entry.get().strip()
        if not amount_text:
            error_label.config(text="Por favor, ingrese un monto.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            error_label.config(text="El monto debe ser un valor numérico.")
            return

        if amount <= 0:
            error_label.config(text="El monto debe ser mayor a 0.")
            return
        
        associated_card = account.cards[0] 
        
        if associated_card.get_pin() != password_text:
            error_label.config(text="Contraseña incorrecta. Operación cancelada.")
            return

        try:
            account.deposit(amount) 
            show_success_screen(client_object, bank, "¡Depósito Exitoso!", "El dinero ha sido abonado a tu cuenta.")
        except Exception as e:
            error_label.config(text=f"Error: {e}")

    tk.Button(content_frame, text="Confirmar Depósito", font=("Courier", 13, "bold"), bg="white", fg="#00296b", relief="flat", command=deposit_gui).pack(anchor="w", pady=10, ipadx=10, ipady=5)

def open_credits_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)
    
    if client_object.age < 18:
        tk.Label(
            content_frame, text="Esta función no está disponible para ti, lo sentimos. \nPrueba más de nuestras funciones:",
            font=("Courier", 14, "bold"), fg="yellow", bg="#00296b", justify="center"
        ).pack(pady=(40,20))
        
        tk.Button(
            content_frame, text="Volver al panel principal", font=("Courier", 14, "bold"), bg="white", fg="#00296b", relief="flat",
            command=lambda: go_to_client_operations(client_object, bank)
        ).pack(pady=10, ipadx=15, ipady=7)
        return
    
    tk.Label(content_frame, text="Solicitud de Crédito", font=("Courier", 18, "bold"), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 20))

    tk.Label(content_frame, text="Monto solicitado:", font=("Courier", 12), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 5))
    credit_amount_entry = tk.Entry(content_frame, font=("Courier", 12))
    credit_amount_entry.pack(anchor="w", pady=(0, 15), ipady=3, fill="x")

    tk.Label(content_frame, text="Plazo (meses):", font=("Courier", 12), fg="white", bg="#00296b").pack(anchor="w", pady=(0, 5))
    months_options = ["6", "12", "24", "36"]
    selected_months = tk.StringVar(value=months_options[1])
    months_menu = tk.OptionMenu(content_frame, selected_months, *months_options)
    months_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    months_menu.pack(anchor="w", pady=(0, 20))

    error_label = tk.Label(content_frame, text="", font=("Courier", 11), fg="red", bg="#00296b")
    error_label.pack(anchor="w", pady=5)

    def request_credit_gui():
        amount_text = credit_amount_entry.get().strip()
        if not amount_text:
            error_label.config(text="Ingrese un monto válido.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            error_label.config(text="El monto debe ser numérico.")
            return

        if amount < 100000: 
            error_label.config(text="El monto mínimo de crédito es $100,000.")
            return

        show_success_screen(client_object, bank, "¡Crédito en Estudio!", f"Tu solicitud por ${amount:,.2f} a {selected_months.get()} meses está siendo evaluada.")

    tk.Button(content_frame, text="Solicitar Crédito", font=("Courier", 13, "bold"), bg="white", fg="#00296b", relief="flat", command=request_credit_gui).pack(anchor="w", pady=10, ipadx=10, ipady=5)

def show_success_screen(client_object, bank, title, message):
    clean_screen()

    tk.Label(databank_app, text=title, font=("Courier", 26, "bold"), fg="white", bg="#00296b").pack(pady=(150, 20))
    tk.Label(databank_app, text=message, font=("Courier", 14), fg="white", bg="#00296b", justify="center").pack(pady=(0, 40))

    tk.Button(
        databank_app, text="Volver al panel", font=("Courier", 14, "bold"), bg="white", fg="#00296b", relief="flat",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=10, ipadx=15, ipady=7)

def open_cards_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)

    accounts = bank.list_objects.list_accounts_by_client(client_object)

    if not accounts:
        tk.Label(
            content_frame, text="No tienes tarjetas activas.\nCrea una cuenta para asignarte una tarjeta.",
            font=("Courier", 14, "bold"), fg="yellow", bg="#00296b", justify="center"
        ).pack(pady=(40,20))
        
        tk.Button(
            content_frame, text="Volver al panel principal", font=("Courier", 14, "bold"), bg="white", fg="#00296b", relief="flat",
            command=lambda: go_to_client_operations(client_object, bank)
        ).pack(pady=10, ipadx=15, ipady=7)
        return

    main_account = accounts[0]
    has_card = False
    real_card = None

    if hasattr(main_account, 'cards') and main_account.cards:
        real_card = main_account.cards[0]
        has_card = True
        
        card_number = getattr(real_card, 'card_number', "0000000000000000")
        card_cvv = getattr(real_card, 'cvv', "000")
        
        expiration_date = main_account.creation_date + timedelta(days=5*365)
        card_expiration = expiration_date.strftime("%m/%y")
    else:
        card_number = "No asignada"
        card_cvv = "---"
        card_expiration = "MM/YY"

    masked_number = f"**** **** **** {str(card_number)[-4:]}"

    left_container = tk.Frame(content_frame, bg="#00296b")
    left_container.pack(side="left", fill="both", expand=True)

    card_body = tk.Frame(left_container, bg="#00183f", bd=2, relief="solid", width=220, height=360)
    card_body.pack_propagate(False) # forzar tamaño estricto vertical
    card_body.pack(pady=20, anchor="center")

    tk.Label(
        card_body, text="D\nA\nT\nA\nB\nA\nN\nK", font=("Courier", 18, "bold"),
        fg="white", bg="#00183f", justify="center"
    ).pack(side="left", padx=15, pady=20, anchor="n")

    if has_card and real_card and getattr(real_card, "is_blocked", False):
        tk.Label(
            card_body, text="❌ BLOQUEADA", font=("Courier", 12, "bold"),
            fg="red", bg="#00183f"
        ).place(x=85, y=20)

    card_data_frame = tk.Frame(card_body, bg="#00183f")
    card_data_frame.pack(side="bottom", fill="x", padx=10, pady=20)

    tk.Label(
        card_data_frame, text=f"No. Tarjeta:\n{masked_number}", 
        font=("Courier", 11, "bold"), fg="white", bg="#00183f", anchor="w", justify="left"
    ).pack(fill="x", pady=5)

    tk.Label(
        card_data_frame, text=f"CVV: {card_cvv}", 
        font=("Courier", 11), fg="white", bg="#00183f", anchor="w"
    ).pack(fill="x")

    tk.Label(
        card_data_frame, text=f"Vence: {card_expiration}", 
        font=("Courier", 11), fg="white", bg="#00183f", anchor="w"
    ).pack(fill="x", pady=5)

    right_container = tk.Frame(content_frame, bg="#00296b")
    right_container.pack(side="right", fill="both", expand=True)

    action_button_style = {
        "font": ("Courier", 14, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white",
        "width": 22
    }

    actions_inner_frame = tk.Frame(right_container, bg="#00296b")
    actions_inner_frame.pack(expand=True)

    def process_renovation(client_object, bank, card_obj):
        if card_obj:
            try:
                bank.manage_cards.block_card(card_obj)
            except Exception as e:
                print(f"Error al renovar tarjeta: {e}")
        show_success_screen(client_object, bank, "Has solicitado la renovación de tu tarjeta", "Te estaremos manteniendo al tanto del proceso.")
        
        if not hasattr(client_object, 'requests_history'):
            client_object.requests_history = []
        actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        client_object.requests_history.append(f"[{actual}] Solicitud de renovación de Tarjeta No. ****{str(card_obj.card_number)[-4:]}")
        
        show_success_screen(client_object, bank, "Has solicitado la renovación de tu tarjeta", "Te estaremos manteniendo al tanto del proceso.")

    def process_blocking(client_object, bank, card_obj):
        if card_obj:
            try:
                bank.manage_cards.block_card(card_obj)
            except Exception as e:
                print(f"Error al bloquear en backend: {e}")
        
        if not hasattr(client_object, 'requests_history'):
            client_object.requests_history = []
        actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        client_object.requests_history.append(f"[{actual}] Bloqueo preventivo de Tarjeta No. ****{str(card_obj.card_number)[-4:]}")
        show_success_screen(client_object, bank, "Has solicitado el bloqueo de tu tarjeta", "Por mensaje te informaremos del proceso.")

    tk.Button(
        actions_inner_frame, text="Solicitar renovación",
        command=lambda: process_renovation(client_object, bank, real_card),
        **action_button_style
    ).pack(pady=15, ipady=8)
    
    tk.Button(
        actions_inner_frame, text="Bloquear tarjeta",
        command=lambda: process_blocking(client_object, bank, real_card),
        **action_button_style
    ).pack(pady=15, ipady=8)   

def open_faq_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(
        databank_app, 
        bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame,
        text="Preguntas Frecuentes",
        font=("Courier", 20, "bold"),
        fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 20))

    faq_list = [
        {
            "question": "¿Cómo puedo abrir una cuenta en DataBank?",
            "answer": "Para abrir una cuenta, ingresa tu nombre en la pantalla principal, selecciona 'Crear nueva cuenta', completa tus datos personales y autoriza el tratamiento de datos. ¡El sistema te generará un número de cuenta único al instante!"
        },
        {
            "question": "¿Qué comisiones cobran por transferencias?",
            "answer": "Las transferencias entre cuentas propias o de otros clientes de DataBank son completamente gratuitas. Si excedes el límite transaccional por minuto de tu tipo de cuenta, el sistema podría pausar tus operaciones temporalmente por seguridad."
        },
        {
            "question": "¿Cómo recupero mi contraseña de la tarjeta?",
            "answer": "Por motivos de seguridad, los pines de las tarjetas se asignan durante el proceso de apertura. Si deseas recuperarlo o renovarlo, puedes solicitar una renovación de tarjeta física o contactar al Director de la sucursal."
        }
    ]

  
    def create_accordion_item(parent_frame, question_text, answer_text):
        item_frame = tk.Frame(
            parent_frame, bg="#00183f", 
            bd=1, 
            relief="solid")
        item_frame.pack(fill="x", pady=8, ipady=5)

        header_frame = tk.Frame(item_frame, bg="#00183f")
        header_frame.pack(fill="x", padx=15, pady=5)

        question_label = tk.Label(
            header_frame, 
            text=question_text, 
            font=("Courier", 11, "bold"),
            fg="white", 
            bg="#00183f", 
            anchor="w"
        )
        question_label.pack(side="left", fill="x", expand=True)

        #este label está oculto por defecto, puesto que no es hasta que el cliente da clic que se visibiliza
        answer_label = tk.Label(
            item_frame, 
            text=answer_text, 
            font=("Courier", 10),
            fg="#9C9C9C", 
            bg="#00183f", 
            anchor="w", 
            justify="left",
            wraplength=480  # ajusta la línea para que no se desborde la interfaz
        )

        arrow_button = tk.Button(
            header_frame, 
            text="▼", 
            font=("Courier", 12, "bold"),
            fg="white", 
            bg="#00183f", 
            relief="flat", 
            bd=0,
            activebackground="#00183f", 
            activeforeground="yellow",
            cursor="hand2"
        )

        def toggle_accordion():
            if answer_label.winfo_manager(): 
                answer_label.pack_forget()
                arrow_button.config(text="▼", fg="white")
            else:
                answer_label.pack(fill="x", padx=15, pady=(5, 10), anchor="w")
                arrow_button.config(text="▲", fg="yellow")

        #si se le da clic tanto al texto como al icono funciona
        arrow_button.config(command=toggle_accordion)
        question_label.bind("<Button-1>", lambda event: toggle_accordion()) #<button-1> es el clic izquierdo del mouse

        arrow_button.pack(side="right", padx=5)

    for item in faq_list:
        create_accordion_item(content_frame, item["question"], item["answer"])

def open_my_account_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)
    
    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(
        content_frame, text="Mis Datos Personales",
        font=("Courier", 20, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 25))

    if hasattr(client_object, 'registration_date') and client_object.registration_date:
        formatted_date = client_object.registration_date.strftime("%d/%m/%Y")
    else:
        formatted_date = datetime.now().strftime("%d/%m/%Y")

    profile_card = tk.LabelFrame(
        content_frame, text=" Perfil de Usuario ",
        font=("Courier", 14, "bold"), fg="yellow", bg="#00183f",
        padx=20, pady=20, relief="solid", bd=1
    )
    profile_card.pack(fill="x", pady=10)

    img_container = tk.Frame(profile_card, bg="#00183f")
    img_container.pack(side="left", padx=(10, 15), anchor="n")

    try:
        profile = tk.PhotoImage(file="perfil.png")

        profile_img = profile.subsample(3,3)

        img_label = tk.Label(img_container, image=profile_img, bg="#00183f")
        img_label.image = profile_img # type: ignore
        img_label.pack()

    except Exception as e:
        image_label = tk.Label(
            img_container, 
            text="👤", 
            font=("Courier", 60), 
            fg="white", 
            bg="#00183f"
        )
        image_label.pack()

    info_container = tk.Frame(profile_card, bg="#00183f")
    info_container.pack(side="left", anchor="n")

    user_data_entries = [
        ("Nombre Completo:", client_object.name),
        ("Documento (DNI):", str(client_object.dni)),
        ("Edad Registrada:", f"{client_object.age} años"),
        ("Profesión / Ocupación:", client_object.profession),
        ("Miembro desde:", formatted_date)
    ]

    for label_title, label_value in user_data_entries:
        row_frame = tk.Frame(profile_card, bg="#00183f")
        row_frame.pack(fill="x", pady=6)

        tk.Label(
            row_frame, text=label_title, font=("Courier", 11, "bold"),
            fg="#9C9C9C", bg="#00183f", anchor="w", width=22
        ).pack(side="left")

        tk.Label(
            row_frame, text=label_value, font=("Courier", 12, "bold"),
            fg="white", bg="#00183f", anchor="w"
        ).pack(side="left")

    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=30, ipadx=12, ipady=6)

def open_history_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame, text="Historial de Transacciones",
        font=("Courier", 18, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 15))

    accounts = bank.list_objects.list_accounts_by_client(client_object)

    if not accounts:
        tk.Label(
            content_frame, text="No tienes cuentas registradas para ver el historial.",
            font=("Courier", 14, "bold"), fg="yellow", bg="#00296b"
        ).pack(anchor="w", pady=20)

        tk.Button(
            content_frame, text="Volver al panel principal",
            font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
            command=lambda: go_to_client_operations(client_object, bank)
        ).pack(pady=20, ipadx=12, ipady=6)
        return
    
    selector_frame = tk.Frame(content_frame, bg="#00296b")
    selector_frame.pack(anchor="w", pady=(0, 15))

    tk.Label(
        selector_frame, text="Selecciona una cuenta:",
        font=("Courier", 12, "bold"), fg="white", bg="#00296b"
    ).pack(side="left", padx=(0, 10))

    def label_for(account_obj):
        num = str(account_obj.account_number)
        return f"{type(account_obj).__name__} - ****{num[-4:]}"

    account_labels = [label_for(a) for a in accounts]
    selected_account_var = tk.StringVar(value=account_labels[0])

    def on_account_change(_):
        render_history_entries()

    account_menu = tk.OptionMenu(selector_frame, selected_account_var, *account_labels, command=on_account_change)
    account_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    account_menu.pack(side="left")

    history_card = tk.Frame(content_frame, bg="#f5ebe0", bd=1, relief="solid")
    history_card.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(history_card, bg="#f5ebe0", highlightthickness=0)
    scrollbar = tk.Scrollbar(history_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5ebe0")

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")

    def get_selected_account():
        idx = account_labels.index(selected_account_var.get())
        return accounts[idx]

    def render_history_entries():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        active_account = get_selected_account()
    
        transactions_list = []
        if hasattr(active_account, 'transactions'):
            transactions_list = active_account.transactions
        elif hasattr(active_account, 'history'):
            transactions_list = active_account.history

        if transactions_list:
            for index, transaction in enumerate(transactions_list):
                row_frame = tk.Frame(scrollable_frame, bg="#f5ebe0")
                row_frame.pack(fill="x", pady=4, anchor="w")

                transaction_text = f"{index + 1}. {str(transaction)}"

                tk.Label(
                    row_frame, text=transaction_text,
                    font=("Courier", 10, "bold"), fg="#00296b", bg="#f5ebe0",
                    anchor="w", justify="left"
                ).pack(side="left")
        else:
            tk.Label(
                scrollable_frame, text="No hay transacciones registradas en esta cuenta.",
                font=("Courier", 11, "italic"), fg="#8b7e74", bg="#f5ebe0"
            ).pack(pady=40, padx=20, anchor="center")

    render_history_entries()

    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=15, ipadx=12, ipady=6)

def solicitudes_report(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame, text="Historial de Solicitudes",
        font=("Courier", 18, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 15))

    requests_card = tk.Frame(content_frame, bg="#f5ebe0", bd=1, relief="solid")
    requests_card.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(requests_card, bg="#f5ebe0", highlightthickness=0)
    scrollbar = tk.Scrollbar(requests_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5ebe0")

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")

    requests_list = getattr(client_object, 'requests_history', [])

    if requests_list:
        for index, request_text in enumerate(requests_list):
            row_frame = tk.Frame(scrollable_frame, bg="#f5ebe0")
            row_frame.pack(fill="x", pady=4, anchor="w")

            tk.Label(
                row_frame, text=f"{index + 1}. {request_text}",
                font=("Courier", 10, "bold"), fg="#00296b", bg="#f5ebe0",
                anchor="w", justify="left"
            ).pack(side="left")
    else:
        tk.Label(
            scrollable_frame, text="No has realizado ninguna solicitud en esta sesión.",
            font=("Courier", 11, "italic"), fg="#8b7e74", bg="#f5ebe0"
        ).pack(pady=40, padx=20, anchor="center")

    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=15, ipadx=12, ipady=6)
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame, text="Historial de Solicitudes",
        font=("Courier", 18, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 15))

    accounts = bank.list_objects.list_accounts_by_client(client_object)

    if not accounts:
        tk.Label(
            content_frame, text="No tienes cuentas registradas para ver solicitudes.",
            font=("Courier", 14, "bold"), fg="yellow", bg="#00296b"
        ).pack(anchor="w", pady=20)

        tk.Button(
            content_frame, text="Volver al panel principal",
            font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
            command=lambda: go_to_client_operations(client_object, bank)
        ).pack(pady=20, ipadx=12, ipady=6)
        return
    
    selector_frame = tk.Frame(content_frame, bg="#00296b")
    selector_frame.pack(anchor="w", pady=(0, 15))

    tk.Label(
        selector_frame, text="Selecciona una cuenta:",
        font=("Courier", 12, "bold"), fg="white", bg="#00296b"
    ).pack(side="left", padx=(0, 10))

    def label_for(account_obj):
        num = str(account_obj.account_number)
        return f"{type(account_obj).__name__} - ****{num[-4:]}"

    account_labels = [label_for(a) for a in accounts]
    selected_account_var = tk.StringVar(value=account_labels[0])

    def on_account_change(_):
        render_requests_entries()

    account_menu = tk.OptionMenu(selector_frame, selected_account_var, *account_labels, command=on_account_change)
    account_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    account_menu.pack(side="left")

    requests_card = tk.Frame(content_frame, bg="#f5ebe0", bd=1, relief="solid")
    requests_card.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(requests_card, bg="#f5ebe0", highlightthickness=0)
    scrollbar = tk.Scrollbar(requests_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5ebe0")

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")

    def get_selected_account():
        idx = account_labels.index(selected_account_var.get())
        return accounts[idx]

    def render_requests_entries():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        active_account = get_selected_account()
    
        all_activities = []
        if hasattr(active_account, 'transactions'):
            all_activities = active_account.transactions
        elif hasattr(active_account, 'history'):
            all_activities = active_account.history

        keywords = ["solicitud", "bloqueo", "desbloqueo", "creacion", "creación", "renovación", "renovacion"]
        requests_list = [
            activity for activity in all_activities 
            if any(key in str(activity).lower() for key in keywords)
        ]

        if requests_list:
            for index, request in enumerate(requests_list):
                row_frame = tk.Frame(scrollable_frame, bg="#f5ebe0")
                row_frame.pack(fill="x", pady=4, anchor="w")

                request_text = f"{index + 1}. {str(request)}"

                tk.Label(
                    row_frame, text=request_text,
                    font=("Courier", 10, "bold"), fg="#00296b", bg="#f5ebe0",
                    anchor="w", justify="left"
                ).pack(side="left")
        else:
            tk.Label(
                scrollable_frame, text="No has realizado ninguna solicitud en esta cuenta.",
                font=("Courier", 11, "italic"), fg="#8b7e74", bg="#f5ebe0"
            ).pack(pady=40, padx=20, anchor="center")

    render_requests_entries()

    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=15, ipadx=12, ipady=6)

def open_requests_module(client_object, bank):
    clean_screen()
    build_nav_bar(client_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame, text="Historial de Solicitudes",
        font=("Courier", 18, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 15))

    requests_card = tk.Frame(content_frame, bg="#f5ebe0", bd=1, relief="solid")
    requests_card.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(requests_card, bg="#f5ebe0", highlightthickness=0)
    scrollbar = tk.Scrollbar(requests_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5ebe0")

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")

    requests_list = getattr(client_object, 'requests_history', [])

    if requests_list:
        for index, request_text in enumerate(requests_list):
            row_frame = tk.Frame(scrollable_frame, bg="#f5ebe0")
            row_frame.pack(fill="x", pady=4, anchor="w")

            tk.Label(
                row_frame, text=f"{index + 1}. {request_text}",
                font=("Courier", 10, "bold"), fg="#00296b", bg="#f5ebe0",
                anchor="w", justify="left"
            ).pack(side="left")
    else:
        tk.Label(
            scrollable_frame, text="No has realizado ninguna solicitud en esta sesión.",
            font=("Courier", 11, "italic"), fg="#8b7e74", bg="#f5ebe0"
        ).pack(pady=40, padx=20, anchor="center")

    # Botón de Volver
    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_client_operations(client_object, bank)
    ).pack(pady=15, ipadx=12, ipady=6)

def go_to_employee_login_screen(username,bank):
    clean_screen()

    tk.Label(
        databank_app,
        text="Acceso de Empleados",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=40)

    tk.Label(
        databank_app,
        text="Ingrese su Número de DNI / Cédula:",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(pady=10)

    entry_dni = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_dni.pack(pady=10)
    entry_dni.focus() #hace que el cursor aparezca listo para escribir (falta implementarlo en los otros)

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=10)

    def verify_dni(event=None):
        dni_text = entry_dni.get().strip()
        if not dni_text.isdigit():
            label_error.config(text="El DNI debe contener solo números.")
            return

        dni = int(dni_text)

        employee_found = bank.search.search_employee_by_dni(dni)
        if employee_found:
            go_to_employee_password_screen(employee_found, bank, username)
            print("Cliente encontrado")
        else:
            go_to_register_employee_screen(dni, bank)

    entry_dni.bind("<Return>", verify_dni)

    tk.Button(
        databank_app,
        text="Continuar",
        font=("Courier", 12, "bold"),
        bg="white", fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=verify_dni
    ).pack(pady=20, ipadx=15, ipady=5)

    tk.Button(
        databank_app,
        text="⬅ Volver al Inicio",
        font=("Courier", 10, "bold"),
        bg="#00296b", fg="white", # Fondo azul para que no compita visualmente con el botón blanco
        relief="flat",
        activebackground="#00183f", activeforeground="white",
        command=lambda: go_to_main_menu(username) # O como se llame tu pantalla de inicio principal
    ).pack(pady=5)

def go_to_employee_password_screen(employee, bank, username):
    clean_screen()

    tk.Label(
        databank_app,
        text=f"¡Hola de nuevo, {username}!",
        font=("Courier", 18, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=30)

    tk.Label(
        databank_app,
        text="Por favor, ingresa tu contraseña de acceso:",
        font=("Courier", 12), fg="white", bg="#00296b"
    ).pack(pady=10)

    entry_password = tk.Entry(databank_app, font=("Courier", 12), show="*", justify="center")
    entry_password.pack(pady=10)
    entry_password.focus()

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=10)

    def validate_password(event=None):
        password_text = entry_password.get().strip()

        if not password_text:
            label_error.config(text="La contraseña no puede estar vacía.")
            return

        if str(password_text) == str(employee.get_password()):
            print(f"Login exitoso para el empleado: {employee.name}")
            go_to_employee_operations(employee, bank)
        else:
            label_error.config(text="Contraseña incorrecta. Inténtalo de nuevo.")

    entry_password.bind("<Return>", validate_password)

    tk.Button(
        databank_app,
        text="Iniciar Sesión",
        font=("Courier", 12, "bold"),
        bg="white", fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=validate_password
    ).pack(pady=20, ipadx=15, ipady=5)

    tk.Button(
        databank_app,
        text="⬅ Cambiar de usuario / Volver",
        font=("Courier", 10, "bold"),
        bg="#00296b", fg="white",
        relief="flat",
        activebackground="#00183f", activeforeground="white",
        command=lambda: go_to_employee_login_screen(username, bank)
    ).pack(pady=5)

def go_to_register_employee_screen(dni, bank):
    clean_screen()

    tk.Label(
        databank_app,
        text="¡Gracias por querer ser parte de nuestro equipo!",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20)

    tk.Label(
        databank_app, 
        text=f"DNI / Cédula identificada: {dni}", 
        font=("Courier", 12, "italic"), 
        fg="yellow", 
        bg="#00296b"
    ).pack(pady=5)

    tk.Label(databank_app, text="Nombres:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    entry_names = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_names.pack(pady=5)

    tk.Label(databank_app, text="Apellidos:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    entry_lastnames = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_lastnames.pack(pady=5)

    tk.Label(databank_app, text="Años de Experiencia:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    entry_experience = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_experience.pack(pady=5)

    tk.Label(databank_app, text="Contraseña de Acceso:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    entry_password = tk.Entry(databank_app, font=("Courier", 12), show="*", justify="center")
    entry_password.pack(pady=5)

    tk.Label(databank_app, text="Rol / Cargo:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    
    roles = ["Administrativo", "Analista", "Logistica", "Director"]
    selected_role_var = tk.StringVar(value=roles[0])

    role_menu = tk.OptionMenu(databank_app, selected_role_var, *roles)
    role_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    role_menu.pack(pady=5)

    dept_frame = tk.Frame(databank_app, bg="#00296b")
    tk.Label(dept_frame, text="Departamento (Área):", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=5)
    entry_department = tk.Entry(dept_frame, font=("Courier", 12), justify="center")
    entry_department.pack(pady=5)

    def toggle_department_field(*args):
        if selected_role_var.get() == "Director":
            dept_frame.pack(pady=5) 
        else:
            dept_frame.pack_forget() 
            entry_department.delete(0, tk.END)

    selected_role_var.trace_add("write", toggle_department_field)

    data_auth_var = tk.IntVar(value=0) 
    auth_checkbox = tk.Checkbutton(
        databank_app,
        text="Autorizo el tratamiento de mis datos personales\ncon tal de hacer funcionar este proyecto",
        variable=data_auth_var,
        onvalue=1,
        offvalue=0, 
        font=("Courier", 10),
        fg="white",
        bg="#00296b",
        activebackground="#00296b",
        activeforeground="white",
        selectcolor="#00183f", 
        justify="center"
    )
    auth_checkbox.pack(pady=15)
    auth_checkbox.variable = data_auth_var

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=5)

    def save_new_employee(dni):
        names = entry_names.get().strip()
        lastnames = entry_lastnames.get().strip()
        exp_text = entry_experience.get().strip()
        password = entry_password.get().strip()
        role = selected_role_var.get()
        department = entry_department.get().strip()

        if not names or not lastnames or not exp_text or not password:
            label_error.config(text="Todos los campos son obligatorios. Asegúrese de que no falte alguno.")
            return
        
        if role == "Director" and not department:
            label_error.config(text="El departamento es obligatorio para el cargo de Director.")
            return
        
        if auth_checkbox.variable.get() == 0:
            label_error.config(text="Debe autorizar el tratamiento de datos para continuar.")
            return

        try:
            experience = int(exp_text)
            full_name = f"{names} {lastnames}"
            role_lower = role.lower()

            if role_lower == "administrativo":
                employee_role_obj = Administrative(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "analista":
                employee_role_obj = Analist(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "logistica":
                employee_role_obj = Logistic(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "director":
                employee_role_obj = Director(name=full_name, dni=dni, department=department, experience=experience, password=password)
            else:
                label_error.config(text="Rol seleccionado no válido.")
                return

            authorizer = bank.search.search_employee_by_dni(1021678463)

            if not authorizer:
                laura_cargo = Director(name="Laura Espinosa", dni=1021678463, department="Ingeniería", experience=1, password="julilaura")
                if not hasattr(bank, 'employees'):
                    bank.employees = []
                bank.employees.append(laura_cargo)
                authorizer = laura_cargo

            bank.manage_employees.add_employee(authorizer, employee_role_obj)

            print(f"Nuevo objeto Empleado guardado en el backend para {full_name} con cargo {role}.")
            go_to_employee_operations(employee_role_obj, bank)

        except ValueError:
            label_error.config(text="La experiencia debe ser un número entero válido.")
        except Exception as e:
            label_error.config(text=f"Error al registrar: {e}")

    tk.Button(
        databank_app,
        text="Continuar",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        command= lambda : save_new_employee(dni),
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white"
    ).pack(pady=20, ipadx=10, ipady=5)

def go_to_employee_operations(employee_role_obj, bank):
    clean_screen()

    if isinstance(employee_role_obj, Analist):
        render_analist_panel(employee_role_obj, bank)
    elif isinstance(employee_role_obj, Logistic):
        render_logistic_panel(employee_role_obj, bank)
    elif isinstance(employee_role_obj, Administrative):
        render_administrative_panel(employee_role_obj, bank)
    elif isinstance(employee_role_obj, Director):
        render_director_panel(employee_role_obj, bank)

def render_director_panel(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    global raise_img,salary_img,help_img, user_img
    raise_img1 = tk.PhotoImage(file="raising.png")
    salary_img1 = tk.PhotoImage(file="salary.png")
    user_img1 = tk.PhotoImage(file="users.png")
    help_img1 = tk.PhotoImage(file="help.png")

    raise_img = raise_img1.subsample(2,2)
    salary_img = salary_img1.subsample(2,2)
    user_img = user_img1.subsample(2,2)
    help_img = help_img1.subsample(2,2)


    tk.Label(
        databank_app,
        text=f"Panel del Cliente: {employee.name}\nRol : Director",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w")

    tk.Label(
        databank_app,
        text="Tus servicios:",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w")

    menu_operations = tk.Frame(databank_app, bg="#00296b")
    menu_operations.pack(pady=30)

    options_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white"
    }

    tk.Button(
        menu_operations,
        text="\nAceptar ascenso",
        command=lambda: open_asc_module(employee, bank),
        image=raise_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAumentar salarios",
        command=lambda: raise_salaries_module(employee, bank),
        image=salary_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nCrear / eliminar usuario",
        command=lambda: create_add_users(employee, bank),
        image=user_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAyuda",
        command=lambda: open_faq_e_module(employee, bank),
        image=help_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

def render_analist_panel(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    global raise_img,bonus_img,reports_img,help_img
    raise_img1 = tk.PhotoImage(file="raising.png")
    bonus_img1 = tk.PhotoImage(file="bonus.png")
    reports_img1 = tk.PhotoImage(file="report.png")
    help_img1 = tk.PhotoImage(file="help.png")

    raise_img = raise_img1.subsample(2,2)
    bonus_img = bonus_img1.subsample(2,2)
    reports_img = reports_img1.subsample(2,2)
    help_img = help_img1.subsample(2,2)

    tk.Label(
        databank_app,
        text=f"Panel del Empleado: {employee.name}\nRol : Analista",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") 

    tk.Label(
        databank_app,
        text="Tus servicios:",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w")

    menu_operations = tk.Frame(databank_app, bg="#00296b")
    menu_operations.pack(pady=30)

    options_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white"
    }

    tk.Button(
        menu_operations,
        text="\nSolicitar bonus",
        command=lambda: open_bonus_module(employee, bank),
        image=bonus_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nVer reportes",
        command=lambda: open_report_module(employee, bank),
        image=reports_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nSolicitar ascenso.",
        command=lambda: render_promotion_request_panel(employee, bank),
        image=raise_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAyuda",
        command=lambda: open_faq_e_module(employee, bank),
        image=help_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

def render_logistic_panel(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    global raise_img,bonus_img,help_img
    raise_img1 = tk.PhotoImage(file="raising.png")
    bonus_img1 = tk.PhotoImage(file="bonus.png")
    help_img1 = tk.PhotoImage(file="help.png")

    raise_img = raise_img1.subsample(2,2)
    bonus_img = bonus_img1.subsample(2,2)
    help_img = help_img1.subsample(2,2)


    tk.Label(
        databank_app,
        text=f"Panel del Empleado: {employee.name} \nRol : Logística",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") 

    tk.Label(
        databank_app,
        text="Tus servicios:",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") #anchor me ayuda a poner el texto hacia la izquierda

    menu_operations = tk.Frame(databank_app, bg="#00296b")
    menu_operations.pack(pady=30)

    options_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white"
    }

    tk.Button(
        menu_operations,
        text="\nSolicitar bonus",
        command=lambda: open_bonus_module(employee, bank),
        image=bonus_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nSolicitar ascenso",
        command=lambda: render_promotion_request_panel(employee, bank),
        image=raise_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAyuda",
        command=lambda: open_faq_e_module(employee, bank),
        image=help_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

def render_administrative_panel(employee_role_obj, bank):
    clean_screen()
    build_nav_bar_e(employee_role_obj, bank)

    global report_img,bonus_img,help_img
    report_img1 = tk.PhotoImage(file="report.png")
    bonus_img1 = tk.PhotoImage(file="bonus.png")
    help_img1 = tk.PhotoImage(file="help.png")
    user_img1 = tk.PhotoImage(file="users.png")

    report_img = report_img1.subsample(2,2)
    bonus_img = bonus_img1.subsample(2,2)
    help_img = help_img1.subsample(2,2)
    user_img = user_img1.subsample(2,2)

    tk.Label(
        databank_app,
        text=f"Panel del Cliente: {employee_role_obj.name}\nPerfil: \nRol : Director",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w") 
    
    tk.Label(
        databank_app,
        text="Tus servicios:",
        font=("Courier", 19, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20, anchor="w")

    menu_operations = tk.Frame(databank_app, bg="#00296b")
    menu_operations.pack(pady=30)

    options_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white"
    }

    tk.Button(
        menu_operations,
        text="\nSolicitar bonus",
        command=lambda: open_bonus_module(employee_role_obj, bank),
        image=bonus_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nVer reportes",
        command=lambda: open_cards_module(employee_role_obj, bank),
        image=report_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nCrear / eliminar usuario",
        command=lambda: create_add_users(employee_role_obj, bank),
        image=user_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

    tk.Button(
        menu_operations,
        text="\nAyuda",
        command=lambda: open_faq_e_module(employee_role_obj, bank),
        image=help_img,
        compound="top",
        **options_style
    ).pack(side="left", padx=15, ipadx=10, ipady=10)

def render_promotion_request_panel(employee_role_obj, bank):
    clean_screen()
    build_nav_bar_e(employee_role_obj, bank)
    
    current_role = type(employee_role_obj).__name__

    frame_promotion = tk.Frame(databank_app, bg="#00296b")
    frame_promotion.pack(pady=20, padx=20, fill="both", expand=True)

    label_title = tk.Label(
        frame_promotion, 
        text="Solicitud de Ascenso Laboral", 
        font=("Courier", 18, "bold"),
        fg="white",
        bg="#00296b"
    )
    label_title.pack(pady=10)

    label_role = tk.Label(
        frame_promotion, 
        text=f"Actualmente su rol es: {current_role}", 
        font=("Courier", 12),
        fg="yellow",
        bg="#00296b"
    )
    label_role.pack(pady=5)

    label_question = tk.Label(
        frame_promotion, 
        text="¿Desea solicitar un ascenso o bonificación a sus superiores?", 
        font=("Courier", 11),
        fg="white",
        bg="#00296b"
    )
    label_question.pack(pady=10)

    frame_motives = tk.Frame(frame_promotion, bg="#00296b")
    
    label_motives_title = tk.Label(
        frame_motives, 
        text="Especifique los motivos de su solicitud:", 
        font=("Courier", 11, "bold"),
        fg="white",
        bg="#00296b"
    )
    label_motives_title.pack(anchor="w", pady=5)
    
    text_motives = tk.Text(
        frame_motives, 
        height=5, 
        width=40, 
        font=("Courier", 11),
        bg="#00183f",
        fg="white",
        insertbackground="white",
        relief="groove",
        bd=2
    )
    text_motives.pack(pady=5)

    def show_motives_fields():
        btn_yes.pack_forget()
        frame_motives.pack(pady=10)

    btn_yes = tk.Button(
        frame_promotion, 
        text="Sí", 
        bg="#00ff66", 
        fg="#00183f", 
        font=("Courier", 11, "bold"), 
        width=10, 
        relief="flat",
        command=show_motives_fields
    )
    btn_yes.pack(pady=5)

    def send_request():
        motives = text_motives.get("1.0", "end-1c").strip()
        
        if not motives:
            messagebox.showwarning("Campo Vacío", "Por favor, detalle los motivos antes de enviar su solicitud.")
            return

        try:
            new_request = PromotionRequest(employee=employee_role_obj, reasons=motives)
            
            if not hasattr(bank, 'promotion_requests'):
                bank.promotion_requests = []
                
            bank.promotion_requests.append(new_request)

            messagebox.showinfo("Éxito", "Su solicitud de ascenso ha sido enviada con éxito a sus superiores.")
            go_to_employee_operations(employee_role_obj, bank)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la solicitud: {e}")

    btn_send = tk.Button(
        frame_motives, 
        text="Enviar Solicitud", 
        bg="#00ff66", 
        fg="#00183f", 
        font=("Courier", 11, "bold"), 
        relief="flat",
        command=send_request
    )
    btn_send.pack(pady=10, ipadx=10)

    btn_back = tk.Button(
        frame_promotion, 
        text="Regresar", 
        bg="red", 
        fg="white", 
        font=("Courier", 11, "bold"),
        relief="flat",
        command=lambda: go_to_employee_operations(employee_role_obj, bank)
    )
    btn_back.pack(pady=20, ipadx=10)

def open_faq_e_module(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    content_frame = tk.Frame(
        databank_app, 
        bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame,
        text="Preguntas Frecuentes - Empleados",
        font=("Courier", 20, "bold"),
        fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 20))

    faq_list = [
        {
            "question": "¿Cómo se procesa una solicitud de aumento o ascenso?",
            "answer": "Una vez envías tu solicitud detallando los motivos desde tu panel operativo, el sistema la almacena en una lista de peticiones pendientes que únicamente los usuarios con el rol de Director pueden revisar, aprobar o rechazar."
        },
        {
            "question": "¿Qué es el 'percentage increase' y cómo me afecta?",
            "answer": "Es el incremento porcentual aplicado a tu salario base actual. Mantiene el impacto proporcional al cargo que ocupas y se calcula comparando tu nuevo sueldo asignado con el anterior para asegurar un ajuste equitativo."
        },
        {
            "question": "¿Cuáles son las responsabilidades según cada rol?",
            "answer": "Los Administrativos gestionan registros, los Analistas evalúan métricas transaccionales, el equipo de Logística coordina operaciones de distribución y abastecimiento, mientras que el Director supervisa la sucursal y autoriza contrataciones."
        }
    ]

    def create_accordion_item(parent_frame, question_text, answer_text):
        item_frame = tk.Frame(
            parent_frame, bg="#00183f", 
            bd=1, 
            relief="solid")
        item_frame.pack(fill="x", pady=8, ipady=5)

        header_frame = tk.Frame(item_frame, bg="#00183f")
        header_frame.pack(fill="x", padx=15, pady=5)

        question_label = tk.Label(
            header_frame, 
            text=question_text, 
            font=("Courier", 11, "bold"),
            fg="white", 
            bg="#00183f", 
            anchor="w"
        )
        question_label.pack(side="left", fill="x", expand=True)

        answer_label = tk.Label(
            item_frame, 
            text=answer_text, 
            font=("Courier", 10),
            fg="#9C9C9C", 
            bg="#00183f", 
            anchor="w", 
            justify="left",
            wraplength=480  
        )

        arrow_button = tk.Button(
            header_frame, 
            text="▼", 
            font=("Courier", 12, "bold"),
            fg="white", 
            bg="#00183f", 
            relief="flat", 
            bd=0,
            activebackground="#00183f", 
            activeforeground="yellow",
            cursor="hand2"
        )

        def toggle_accordion():
            if answer_label.winfo_manager(): 
                answer_label.pack_forget()
                arrow_button.config(text="▼", fg="white")
            else:
                answer_label.pack(fill="x", padx=15, pady=(5, 10), anchor="w")
                arrow_button.config(text="▲", fg="yellow")

        arrow_button.config(command=toggle_accordion)
        question_label.bind("<Button-1>", lambda event: toggle_accordion()) 

        arrow_button.pack(side="right", padx=5)

    for item in faq_list:
        create_accordion_item(content_frame, item["question"], item["answer"])

def open_bonus_module(employee_role_obj, bank):
    clean_screen()
    build_nav_bar_e(employee_role_obj, bank)
    
    current_role = type(employee_role_obj).__name__

    frame_promotion = tk.Frame(databank_app, bg="#00296b")
    frame_promotion.pack(pady=20, padx=20, fill="both", expand=True)

    label_title = tk.Label(
        frame_promotion, 
        text="Solicitud de Aumento Salarial", 
        font=("Courier", 18, "bold"),
        fg="white",
        bg="#00296b"
    )
    label_title.pack(pady=10)

    label_role = tk.Label(
        frame_promotion, 
        text=f"Actualmente su rol es: {current_role}", 
        font=("Courier", 12),
        fg="yellow",
        bg="#00296b"
    )
    label_role.pack(pady=5)

    label_question = tk.Label(
        frame_promotion, 
        text="¿Desea solicitar un aumento de su salario?", 
        font=("Courier", 11),
        fg="white",
        bg="#00296b"
    )
    label_question.pack(pady=10)

    frame_motives = tk.Frame(frame_promotion, bg="#00296b")
    
    label_motives_title = tk.Label(
        frame_motives, 
        text="Especifique los motivos de su solicitud:", 
        font=("Courier", 11, "bold"),
        fg="white",
        bg="#00296b"
    )
    label_motives_title.pack(anchor="w", pady=5)
    
    text_motives = tk.Text(
        frame_motives, 
        height=5, 
        width=40, 
        font=("Courier", 11),
        bg="#00183f",
        fg="white",
        insertbackground="white",
        relief="groove",
        bd=2
    )
    text_motives.pack(pady=5)

    def show_motives_fields():
        btn_yes.pack_forget()
        frame_motives.pack(pady=10)

    btn_yes = tk.Button(
        frame_promotion, 
        text="Sí", 
        bg="#00ff66", 
        fg="#00183f", 
        font=("Courier", 11, "bold"), 
        width=10, 
        relief="flat",
        command=show_motives_fields
    )
    btn_yes.pack(pady=5)

    def send_request():
        motives = text_motives.get("1.0", "end-1c").strip()
        
        if not motives:
            messagebox.showwarning("Campo Vacío", "Por favor, detalle los motivos antes de enviar su solicitud.")
            return

        try:
            new_request = SalaryIncreaseRequest(employee=employee_role_obj, reasons=motives)
            
            if not hasattr(bank, 'salary_requests'):
                bank.salary_requests = []
                
            bank.salary_requests.append(new_request)

            messagebox.showinfo("¡Gracias por su solicitud!", "Ha sido enviada con éxito a sus superiores.")
            go_to_employee_operations(employee_role_obj, bank)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la solicitud: {e}")

    btn_send = tk.Button(
        frame_motives, 
        text="Enviar Solicitud", 
        bg="#00ff66", 
        fg="#00183f", 
        font=("Courier", 11, "bold"), 
        relief="flat",
        command=send_request
    )
    btn_send.pack(pady=10, ipadx=10)

    btn_back = tk.Button(
        frame_promotion, 
        text="Regresar", 
        bg="red", 
        fg="white", 
        font=("Courier", 11, "bold"),
        relief="flat",
        command=lambda: go_to_employee_operations(employee_role_obj, bank)
    )
    btn_back.pack(pady=20, ipadx=10)

def open_report_module(employee_object, bank):
    clean_screen()
    build_nav_bar_e(employee_object, bank)

    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)

    tk.Label(
        content_frame, text="Módulo de Reportes del Sistema",
        font=("Courier", 18, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 15))

    # --- ZONA DE SELECTORES (BOTONES DE REPORTES) ---
    selector_frame = tk.Frame(content_frame, bg="#00296b")
    selector_frame.pack(anchor="w", pady=(0, 15))

    tk.Label(
        selector_frame, text="Seleccione el tipo de reporte:",
        font=("Courier", 12, "bold"), fg="white", bg="#00296b"
    ).pack(side="left", padx=(0, 15))

    # --- CONTENEDOR VISUAL CON SCROLL (CARD PREMIUM) ---
    report_card = tk.Frame(content_frame, bg="#f5ebe0", bd=1, relief="solid")
    report_card.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(report_card, bg="#f5ebe0", highlightthickness=0)
    scrollbar = tk.Scrollbar(report_card, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5ebe0")

    scrollable_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
    scrollbar.pack(side="right", fill="y")

    # --- LÓGICA DE RENDERIZADO DE LÍNEAS DE REPORTE ---
    def render_report_data(report_lines, empty_message):
        # Limpiamos el scrollable_frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        if report_lines:
            for index, line in enumerate(report_lines):
                row_frame = tk.Frame(scrollable_frame, bg="#f5ebe0")
                row_frame.pack(fill="x", pady=4, anchor="w")

                # Formateamos cada línea del reporte
                line_text = f"{index + 1}. {str(line)}"

                tk.Label(
                    row_frame, text=line_text,
                    font=("Courier", 10, "bold"), fg="#00296b", bg="#f5ebe0",
                    anchor="w", justify="left"
                ).pack(side="left")
        else:
            tk.Label(
                scrollable_frame, text=empty_message,
                font=("Courier", 11, "italic"), fg="#8b7e74", bg="#f5ebe0"
            ).pack(pady=40, padx=20, anchor="center")

    # --- FUNCIONES DISPARADORAS DEL BACKEND ---
    def load_employee_report():
        try:
            # Llamada al backend
            data = bank.report.generate_employee_report()
            render_report_data(data, "No hay registros en el reporte de empleados.")
        except Exception as e:
            render_report_data([f"Error al cargar reporte: {e}"], "Error")

    def load_security_report():
        try:
            # Llamada al backend
            data = bank.report.generate_security_report()
            render_report_data(data, "No hay registros en el reporte de seguridad.")
        except Exception as e:
            render_report_data([f"Error al cargar reporte: {e}"], "Error")

    # --- BOTONES DE ACCIÓN DE LOS REPORTES ---
    btn_employee = tk.Button(
        selector_frame, text="Reporte Empleados",
        font=("Courier", 11, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=load_employee_report
    )
    btn_employee.pack(side="left", padx=5)

    btn_security = tk.Button(
        selector_frame, text="Reporte Seguridad",
        font=("Courier", 11, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=load_security_report
    )
    btn_security.pack(side="left", padx=5)

    # Cargar por defecto el primero para que no abra vacío
    load_employee_report()

    # --- BOTÓN INFERIOR DE SALIDA ---
    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_employee_operations(employee_object, bank)
    ).pack(pady=15, ipadx=12, ipady=6)

def raise_salaries_module(director, bank):
    clean_screen()
    build_nav_bar_e(director, bank)

    tk.Label(
        databank_app,
        text="Módulo de Aumentos Salariales",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=15)

    tk.Label(
        databank_app,
        text="Solicitudes Pendientes de Aprobación:",
        font=("Courier", 12, "italic"),
        fg="yellow",
        bg="#00296b"
    ).pack(pady=5)

    container_frame = tk.Frame(databank_app, bg="#00296b")
    container_frame.pack(pady=10, padx=20, fill="both", expand=True)

    canvas = tk.Canvas(container_frame, bg="#00296b", highlightthickness=0)
    scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#00296b")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    requests_list = getattr(bank, "salary_requests", [])

    if not requests_list:
        no_req_label = tk.Label(
            scrollable_frame,
            text="\n\n>>> No hay solicitudes de aumento de sueldo pendientes.",
            font=("Courier", 13, "bold"),
            fg="#00ff66",
            bg="#00296b",
            justify="center"
        )
        no_req_label.pack(pady=50, fill="x")
    else:
        for req in requests_list:
            req_employee = req.employee
            
            card = tk.Frame(scrollable_frame, bg="#00183f", bd=2, relief="groove")
            card.pack(pady=10, padx=10, fill="x", expand=True)

            info_text = (
                f"Empleado: {req_employee.name} (DNI: {req_employee.dni})\n"
                f"Cargo Actual: {req_employee.__class__.__name__}\n"
                f"Sueldo Actual: ${getattr(req_employee, 'salary', 'No especificado')}\n"
                f"Motivo Aumento: \"{req.reasons}\""
            )
            
            tk.Label(
                card,
                text=info_text,
                font=("Courier", 11),
                fg="white",
                bg="#00183f",
                justify="left",
                anchor="w"
            ).pack(side="left", padx=15, pady=10, fill="x", expand=True)

            btn_frame = tk.Frame(card, bg="#00183f")
            btn_frame.pack(side="right", padx=15, pady=10)

            tk.Button(
                btn_frame,
                text="Aceptar",
                font=("Courier", 10, "bold"),
                bg="#00ff66",
                fg="#00183f",
                relief="flat",
                command=lambda r=req, emp=req_employee: accept_salary_increase(director, bank, r, emp)
            ).pack(pady=5, ipadx=10)

            tk.Button(
                btn_frame,
                text="Rechazar",
                font=("Courier", 10, "bold"),
                bg="red",
                fg="white",
                relief="flat",
                command=lambda r=req: reject_salary_increase(director, bank, r)
            ).pack(pady=5, ipadx=10)

    tk.Button(
        databank_app,
        text="Volver",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: create_add_users(director, bank)
    ).pack(pady=20, ipadx=20, ipady=5)

def accept_salary_increase(director, bank, request, target_employee):
    try:
        target_employee.obtain_bonus()
        
        log_entry = AuditLog(
            action_type="UPDATE",
            operator_name=director.name,
            target_name=target_employee.name,
            target_dni=target_employee.dni,
            details=f"Aumento salarial aprobado. Motivo original: {request.reasons}"
        )
        bank.register_log(log_entry)

        if request in bank.salary_requests:
            bank.salary_requests.remove(request)

        raise_salaries_module(director, bank)

    except Exception as e:
        print(f"Error al procesar el aumento salarial: {e}")

def reject_salary_increase(director, bank, request):
    if request in bank.salary_requests:
        bank.salary_requests.remove(request)
    
    log_entry = AuditLog(
        action_type="REJECT",
        operator_name=director.name,
        target_name=request.employee.name,
        target_dni=request.employee.dni,
        details="Solicitud de aumento salarial rechazada."
    )
    bank.register_log(log_entry)

    raise_salaries_module(director, bank)

def build_nav_bar_e(employee, bank):
    is_menu_open = False

    sidebar_frame = tk.Frame(
        databank_app, 
        bg="#00183f", 
        width=200, 
        height=600
    )
    sidebar_frame.pack_propagate(False) #evita que cambie de tamaño
    sidebar_frame.place_forget() #para que inicie oculto

    tk.Label(
        sidebar_frame, 
        text="Menú", 
        font=("Courier", 14, "bold"), 
        fg="white", bg="#00183f"
    ).pack(pady=20, padx=10)
    
    menu_item_style = {"font": ("Courier", 11), "fg": "white", "bg": "#00183f", "relief": "flat", "anchor": "w"}
    
    tk.Button(
        sidebar_frame, 
        text="👤 Mis datos",
        command=lambda: go_to_employee_operations(employee, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    tk.Button(
        sidebar_frame, 
        text="⚙️ Mi cuenta", 
        command=lambda: open_e_account_module(employee, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    tk.Button(
        sidebar_frame, 
        text="🕒 Historial", 
        command=lambda: view_audit_history(employee, bank), 
        **menu_item_style
    ).pack(fill="x", padx=15, pady=5)

    def toggle_sidebar():
        nonlocal is_menu_open
        if not is_menu_open:
            top_bar_frame.update_idletasks()
            top_bar_height = top_bar_frame.winfo_height()


            sidebar_frame.place(x=0, y=top_bar_height, width=200, height=databank_app.winfo_height() - top_bar_height)
            sidebar_frame.lift()
            menu_button.config(text="✕", bg="#00183f", fg="white") 
            is_menu_open = True
        else:
            sidebar_frame.place_forget()
            menu_button.config(text="☰", bg="#00296b", fg="white") 
            is_menu_open = False

    top_bar_frame = tk.Frame(
        databank_app, 
        bg="#00296b"
    )
    top_bar_frame.pack(fill="x", side="top", anchor="nw")

    menu_button = tk.Button(
        top_bar_frame,
        text="☰",
        font=("Courier", 18, "bold"),
        bg="#00296b",
        fg="white",
        relief="flat",
        activebackground="#00183f",
        activeforeground="white",
        command=toggle_sidebar
    )
    menu_button.pack(side="left", padx=10, pady=10)

    tk.Button(
        top_bar_frame,
        text="Cerrar Sesión",
        font=("Courier", 11),
        bg="#d9534f",
        fg="white",
        relief="flat",
        activebackground="#c9302c",
        activeforeground="white",
        command=lambda: go_to_main_screen(),
    ).pack(pady=20, ipadx=10, ipady=5, side="right")

    databank_label = tk.Label(
        top_bar_frame,
        text="DataBank",
        font=("Courier", 16, "bold"),
        fg="white",
        bg="#00296b",
    )
    databank_label.pack(side="right", padx=20, pady=10)
    databank_label.bind("<Button-1>", lambda event: go_to_employee_operations(employee, bank))

def create_add_users(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    tk.Label(
        databank_app,
        text="Gestión de Personal Interno",
        font=("Courier", 22, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20)

    tk.Label(
        databank_app,
        text=f"Operador: {employee.name}\nSeleccione la acción a realizar:",
        font=("Courier", 13, "italic"),
        fg="yellow",
        bg="#00296b"
    ).pack(pady=10)

    button_style = {
        "font": ("Courier", 13, "bold"),
        "bg": "white",
        "fg": "#00296b",
        "relief": "flat",
        "activebackground": "#9C9C9C",
        "activeforeground": "white",
        "width": 25
    }

    tk.Button(
        databank_app,
        text="Crear Empleado",
        command=lambda: open_get_dni_screen(employee, bank, action_type="create"),
        **button_style
    ).pack(pady=15, ipady=10)

    tk.Button(
        databank_app,
        text="Eliminar Empleado",
        command=lambda: open_get_dni_screen(employee, bank, action_type="delete"),
        **button_style
    ).pack(pady=15, ipady=10)

def open_get_dni_screen(employee, bank, action_type):
    clean_screen()
    build_nav_bar_e(employee, bank)

    title_text = "Registro de Nuevo Personal" if action_type == "create" else "Remover Personal del Sistema"
    
    tk.Label(
        databank_app,
        text=title_text,
        font=("Courier", 18, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20)

    tk.Label(
        databank_app,
        text="Ingrese el DNI / Cédula del objetivo:",
        font=("Courier", 12),
        fg="white",
        bg="#00296b"
    ).pack(pady=10)

    entry_dni = tk.Entry(databank_app, font=("Courier", 14), justify="center")
    entry_dni.pack(pady=10)

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=5)

    def process_dni():
        dni_text = entry_dni.get().strip()
        if not dni_text:
            label_error.config(text="Por favor ingrese un número de identificación.")
            return
        
        try:
            dni_num = int(dni_text)
        except ValueError:
            label_error.config(text="El DNI debe contener solo números.")
            return

        if action_type == "create":
            go_to_add_employee_screen(dni_num, bank, operator=employee)
        
        elif action_type == "delete":
            target_employee = bank.search.search_employee_by_dni(dni_num)
            if not target_employee:
                show_not_found_screen(employee, bank)
            else:
                show_confirm_delete_screen(employee, bank, target_employee)

    tk.Button(
        databank_app,
        text="Continuar",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        command=process_dni
    ).pack(pady=15, ipadx=15, ipady=5)

    tk.Button(
        databank_app,
        text="Cancelar",
        font=("Courier", 11),
        bg="#00183f",
        fg="white",
        relief="flat",
        command=lambda: create_add_users(employee, bank)
    ).pack(pady=5)

def show_confirm_delete_screen(operator, bank, target_employee):
    clean_screen()
    build_nav_bar_e(operator, bank)

    tk.Label(
        databank_app,
        text="Confirmar Eliminación de Personal",
        font=("Courier", 18, "bold"),
        fg="red",
        bg="#00296b"
    ).pack(pady=20)

    info_frame = tk.Frame(databank_app, bg="#00183f", bd=2, relief="groove")
    info_frame.pack(pady=15, padx=20, fill="x")

    label_style = {"font": ("Courier", 12), "fg": "white", "bg": "#00183f", "anchor": "w"}
    
    role_name = target_employee.__class__.__name__

    tk.Label(info_frame, text=f" Vas a eliminar al empleado: {target_employee.name}", **label_style).pack(pady=5, fill="x")
    tk.Label(info_frame, text=f" Con rol: {role_name}", **label_style).pack(pady=5, fill="x")
    tk.Label(info_frame, text=f" Experiencia: {target_employee.experience} años", **label_style).pack(pady=5, fill="x")

    tk.Label(
        databank_app,
        text="Motivos del despido / retiro:",
        font=("Courier", 12, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=10)

    entry_reasons = tk.Entry(databank_app, font=("Courier", 12), width=40, justify="center")
    entry_reasons.pack(pady=5)

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=5)

    def execute_deletion():
        reasons = entry_reasons.get().strip()
        if not reasons:
            label_error.config(text="Por favor, especifique los motivos para proceder.")
            return

        try:
            bank.manage_employees.delete_employee(operator, target_employee)

            log_entry = AuditLog(
                action_type="DELETE",
                operator_name=operator.name,
                target_name=target_employee.name,
                target_dni=target_employee.dni,
                details=reasons
            )
            bank.register_log(log_entry)
            
            clean_screen()
            build_nav_bar_e(operator, bank)
            
            tk.Label(
                databank_app,
                text="¡Proceso Completado!",
                font=("Courier", 18, "bold"),
                fg="white",
                bg="#00296b"
            ).pack(pady=40)
            
            tk.Label(
                databank_app,
                text=f"El empleado {target_employee.name} ha sido removido con éxito.",
                font=("Courier", 12),
                fg="yellow",
                bg="#00296b"
            ).pack(pady=10)
            
            tk.Button(
                databank_app,
                text="Continuar",
                font=("Courier", 12, "bold"),
                bg="white",
                fg="#00296b",
                relief="flat",
                command=lambda: create_add_users(operator, bank)
            ).pack(pady=30, ipadx=15, ipady=5)
            
        except Exception as e:
            label_error.config(text=f"Error de permisos: {e}")

    tk.Button(
        databank_app,
        text="Eliminar usuario",
        font=("Courier", 12, "bold"),
        bg="red",
        fg="white",
        relief="flat",
        command=execute_deletion
    ).pack(pady=15, ipadx=15, ipady=5)

    tk.Button(
        databank_app,
        text="Cancelar",
        font=("Courier", 11),
        bg="#00183f",
        fg="white",
        relief="flat",
        command=lambda: create_add_users(operator, bank)
    ).pack(pady=5)

def show_not_found_screen(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)

    tk.Label(
        databank_app,
        text="Búsqueda sin Resultados",
        font=("Courier", 20, "bold"),
        fg="red",
        bg="#00296b"
    ).pack(pady=40)

    tk.Label(
        databank_app,
        text="No se ha encontrado ese empleado en nuestra base de datos.",
        font=("Courier", 13),
        fg="white",
        bg="#00296b",
        justify="center"
    ).pack(pady=20, padx=20)

    tk.Button(
        databank_app,
        text="Volver",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: create_add_users(employee, bank)
    ).pack(side="bottom", pady=50, ipadx=20, ipady=5)

def go_to_add_employee_screen(dni, bank, operator):
    clean_screen()
    build_nav_bar_e(operator, bank)

    tk.Label(
        databank_app,
        text="Vas a añadir un nuevo empleado",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=15)

    tk.Label(
        databank_app, 
        text=f"DNI / Cédula identificada: {dni}", 
        font=("Courier", 12, "italic"), 
        fg="yellow", 
        bg="#00296b"
    ).pack(pady=5)

    tk.Label(databank_app, text="Nombres:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    entry_names = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_names.pack(pady=2)

    tk.Label(databank_app, text="Apellidos:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    entry_lastnames = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_lastnames.pack(pady=2)

    tk.Label(databank_app, text="Años de Experiencia:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    entry_experience = tk.Entry(databank_app, font=("Courier", 12), justify="center")
    entry_experience.pack(pady=2)

    tk.Label(databank_app, text="Contraseña de Acceso:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    entry_password = tk.Entry(databank_app, font=("Courier", 12), show="*", justify="center")
    entry_password.pack(pady=2)

    tk.Label(databank_app, text="Rol / Cargo:", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    
    roles = ["Administrativo", "Analista", "Logistica", "Director"]
    selected_role_var = tk.StringVar(value=roles[0])

    role_menu = tk.OptionMenu(databank_app, selected_role_var, *roles)
    role_menu.config(font=("Courier", 11), bg="white", fg="#00296b", relief="flat")
    role_menu.pack(pady=2)

    dept_frame = tk.Frame(databank_app, bg="#00296b")
    tk.Label(dept_frame, text="Departamento (Área):", font=("Courier", 12), fg="white", bg="#00296b").pack(pady=2)
    entry_department = tk.Entry(dept_frame, font=("Courier", 12), justify="center")
    entry_department.pack(pady=2)

    def toggle_department_field(*args):
        if selected_role_var.get() == "Director":
            dept_frame.pack(pady=2) 
        else:
            dept_frame.pack_forget() 
            entry_department.delete(0, tk.END)

    selected_role_var.trace_add("write", toggle_department_field)

    data_auth_var = tk.IntVar(value=0) 
    auth_checkbox = tk.Checkbutton(
        databank_app,
        text="Acepto la responsabilidad de añadir un nuevo empleado, con plena autorización de la empresa.",
        variable=data_auth_var,
        onvalue=1,
        offvalue=0, 
        font=("Courier", 10),
        fg="white",
        bg="#00296b",
        activebackground="#00296b",
        activeforeground="white",
        selectcolor="#00183f", 
        justify="center"
    )
    auth_checkbox.pack(pady=10)
    auth_checkbox.variable = data_auth_var

    label_error = tk.Label(databank_app, text="", font=("Courier", 11), fg="red", bg="#00296b")
    label_error.pack(pady=2)

    def save_new_employee(dni):
        names = entry_names.get().strip()
        lastnames = entry_lastnames.get().strip()
        exp_text = entry_experience.get().strip()
        password = entry_password.get().strip()
        role = selected_role_var.get()
        department = entry_department.get().strip()

        if not names or not lastnames or not exp_text or not password:
            label_error.config(text="Todos los campos son obligatorios. Asegúrese de que no falte alguno.")
            return
        
        if role == "Director" and not department:
            label_error.config(text="El departamento es obligatorio para el cargo de Director.")
            return
        
        if auth_checkbox.variable.get() == 0:
            label_error.config(text="Debe autorizar el tratamiento de datos para continuar.")
            return

        try:
            experience = int(exp_text)
            full_name = f"{names} {lastnames}"
            role_lower = role.lower()

            if role_lower == "administrativo":
                employee_role_obj = Administrative(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "analista":
                employee_role_obj = Analist(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "logistica":
                employee_role_obj = Logistic(name=full_name, dni=dni, experience=experience, password=password)
            elif role_lower == "director":
                employee_role_obj = Director(name=full_name, dni=dni, department=department, experience=experience, password=password)
            else:
                label_error.config(text="Rol seleccionado no válido.")
                return

            bank.manage_employees.add_employee(operator, employee_role_obj)
        
            log_entry = AuditLog(
                action_type="CREATE",
                operator_name=operator.name,
                target_name=employee_role_obj.name,
                target_dni=dni,
                details="Nueva contratación en el sistema."
            )
            bank.register_log(log_entry)
            print(f"Nuevo objeto Empleado guardado en el backend para {full_name} con cargo {role}.")
            
            create_add_users(operator, bank)

        except ValueError:
            label_error.config(text="La experiencia debe ser un número entero válido.")
        except Exception as e:
            label_error.config(text=f"Error al registrar: {e}")

    tk.Button(
        databank_app,
        text="Continuar",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        command=lambda: save_new_employee(dni),
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white"
    ).pack(pady=15, ipadx=10, ipady=5)
    
def view_audit_history(employee, bank):
    clean_screen()
    build_nav_bar_e(employee, bank)  

    tk.Label(
        databank_app,
        text="Historial de Auditoría de Personal",
        font=("Courier", 18, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=20)

    history_frame = tk.Frame(databank_app, bg="#00296b")
    history_frame.pack(pady=10, padx=30, fill="both", expand=True)

    text_area = scrolledtext.ScrolledText(
        history_frame,
        wrap=tk.WORD,
        width=80,
        height=15,
        font=("Courier", 11),
        bg="#00183f",
        fg="#00ff66",        
        insertbackground="white",
        relief="flat"
    )
    text_area.pack(fill="both", expand=True, padx=10, pady=10)

    if not hasattr(bank, 'audit_history') or not bank.audit_history:
        text_area.insert(tk.END, ">>> No se registran movimientos en el historial de personal aún.\n")
    else:
        text_area.insert(tk.END, f">>> Mostrando {len(bank.audit_history)} registros de auditoría:\n\n")
        
        for log in reversed(bank.audit_history):
            text_area.insert(tk.END, log.to_string() + "\n")
            text_area.insert(tk.END, "-" * 85 + "\n")

    text_area.config(state=tk.DISABLED) #para que el usuario no modifique en el historial

    tk.Button(
        databank_app,
        text="Volver",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: go_to_employee_operations(employee, bank) 
    ).pack(pady=25, ipadx=20, ipady=5)

def open_e_account_module(employee_role_obj, bank):
    clean_screen()
    build_nav_bar_e(employee_role_obj, bank)
    
    content_frame = tk.Frame(databank_app, bg="#00296b")
    content_frame.pack(fill="both", expand=True, padx=50, pady=30)

    tk.Label(
        content_frame, text="Mis Datos Personales",
        font=("Courier", 20, "bold"), fg="white", bg="#00296b"
    ).pack(anchor="w", pady=(0, 25))

    if hasattr(employee_role_obj, 'registration_date') and employee_role_obj.registration_date:
        formatted_date = employee_role_obj.registration_date.strftime("%d/%m/%Y")
    else:
        formatted_date = datetime.now().strftime("%d/%m/%Y")

    profile_card = tk.LabelFrame(
        content_frame, text=" Perfil de Empleado ",
        font=("Courier", 14, "bold"), fg="yellow", bg="#00183f",
        padx=20, pady=20, relief="solid", bd=1
    )
    profile_card.pack(fill="x", pady=10)

    img_container = tk.Frame(profile_card, bg="#00183f")
    img_container.pack(side="left", padx=(10, 15), anchor="n")

    try:
        profile = tk.PhotoImage(file="perfil.png")
        profile_img = profile.subsample(3, 3)
        img_label = tk.Label(img_container, image=profile_img, bg="#00183f")
        img_label.image = profile_img  # type: ignore
        img_label.pack()
    except Exception:
        image_label = tk.Label(
            img_container, 
            text="👤", 
            font=("Courier", 60), 
            fg="white", 
            bg="#00183f"
        )
        image_label.pack()

    info_container = tk.Frame(profile_card, bg="#00183f")
    info_container.pack(side="left", anchor="n")

    current_role = type(employee_role_obj).__name__
    
    user_data_entries = [
        ("Nombre Completo:", employee_role_obj.name),
        ("Documento (DNI):", str(employee_role_obj.dni)),
        ("Cargo / Rol:", current_role),
        ("Años Experiencia:", f"{employee_role_obj.experience} años"),
        ("Miembro desde:", formatted_date)
    ]

    department = getattr(employee_role_obj, 'department', None)
    if department:
        user_data_entries.insert(3, ("Departamento:", department))

    for label_title, label_value in user_data_entries:
        row_frame = tk.Frame(profile_card, bg="#00183f")
        row_frame.pack(fill="x", pady=6)

        tk.Label(
            row_frame, text=label_title, font=("Courier", 11, "bold"),
            fg="#9C9C9C", bg="#00183f", anchor="w", width=22
        ).pack(side="left")

        tk.Label(
            row_frame, text=label_value, font=("Courier", 12, "bold"),
            fg="white", bg="#00183f", anchor="w"
        ).pack(side="left")

    tk.Button(
        content_frame, text="Volver al panel principal",
        font=("Courier", 12, "bold"), bg="white", fg="#00296b", relief="flat",
        activebackground="#9C9C9C", activeforeground="white",
        command=lambda: go_to_employee_operations(employee_role_obj, bank)
    ).pack(pady=30, ipadx=12, ipady=6)

def open_asc_module(director, bank):
    clean_screen()
    build_nav_bar_e(director, bank)

    tk.Label(
        databank_app,
        text="Módulo de Ascensos y Bonificaciones",
        font=("Courier", 20, "bold"),
        fg="white",
        bg="#00296b"
    ).pack(pady=15)

    tk.Label(
        databank_app,
        text="Solicitudes Pendientes de Aprobación:",
        font=("Courier", 12, "italic"),
        fg="yellow",
        bg="#00296b"
    ).pack(pady=5)

    container_frame = tk.Frame(databank_app, bg="#00296b")
    container_frame.pack(pady=10, padx=20, fill="both", expand=True)

    canvas = tk.Canvas(container_frame, bg="#00296b", highlightthickness=0)
    scrollbar = tk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#00296b")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    requests_list = getattr(bank, "promotion_requests", [])

    if not requests_list:
        no_req_label = tk.Label(
            scrollable_frame,
            text="\n\n>>> No hay solicitudes de ascenso pendientes por el momento.",
            font=("Courier", 13, "bold"),
            fg="#00ff66",
            bg="#00296b",
            justify="center"
        )
        no_req_label.pack(pady=50, fill="x")
    else:
        for req in requests_list:
            req_employee = req.employee
            
            card = tk.Frame(scrollable_frame, bg="#00183f", bd=2, relief="groove")
            card.pack(pady=10, padx=10, fill="x", expand=True)

            info_text = (
                f"Empleado: {req_employee.name} (DNI: {req_employee.dni})\n"
                f"Cargo Actual: {req_employee.__class__.__name__}\n"
                f"Experiencia: {req_employee.experience} años\n"
                f"Motivo Solicitud: \"{req.reasons}\""
            )
            
            tk.Label(
                card,
                text=info_text,
                font=("Courier", 11),
                fg="white",
                bg="#00183f",
                justify="left",
                anchor="w"
            ).pack(side="left", padx=15, pady=10, fill="x", expand=True)

            btn_frame = tk.Frame(card, bg="#00183f")
            btn_frame.pack(side="right", padx=15, pady=10)

            tk.Button(
                btn_frame,
                text="Aceptar",
                font=("Courier", 10, "bold"),
                bg="#00ff66",
                fg="#00183f",
                relief="flat",
                command=lambda r=req, emp=req_employee: accept_promotion(director, bank, r, emp)
            ).pack(pady=5, ipadx=10)

            tk.Button(
                btn_frame,
                text="Rechazar",
                font=("Courier", 10, "bold"),
                bg="red",
                fg="white",
                relief="flat",
                command=lambda r=req: reject_promotion(director, bank, r)
            ).pack(pady=5, ipadx=10)

    tk.Button(
        databank_app,
        text="Volver",
        font=("Courier", 12, "bold"),
        bg="white",
        fg="#00296b",
        relief="flat",
        activebackground="#9C9C9C",
        activeforeground="white",
        command=lambda: create_add_users(director, bank)
    ).pack(pady=20, ipadx=20, ipady=5)

def accept_promotion(director, bank, request, target_employee):
    try:
        target_employee.obtain_bonus()
        
        log_entry = AuditLog(
            action_type="UPDATE",
            operator_name=director.name,
            target_name=target_employee.name,
            target_dni=target_employee.dni,
            details=f"Ascenso/Bono aprobado. Motivo original: {request.reasons}"
        )
        bank.register_log(log_entry)

        if request in bank.promotion_requests:
            bank.promotion_requests.remove(request)

        open_asc_module(director, bank)

    except Exception as e:
        print(f"Error al procesar el ascenso: {e}")

def reject_promotion(director, bank, request):
    if request in bank.promotion_requests:
        bank.promotion_requests.remove(request)
    
    log_entry = AuditLog(
        action_type="REJECT",
        operator_name=director.name,
        target_name=request.employee.name,
        target_dni=request.employee.dni,
        details="Solicitud de ascenso rechazada."
    )
    bank.register_log(log_entry)

    open_asc_module(director, bank)
    
def on_close():
    bank.export_data_json()
    databank_app.destroy()

databank_app.protocol("WM_DELETE_WINDOW", on_close)


databank_app.mainloop() #para que se refresque segun las acciones