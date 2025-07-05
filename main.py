import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Configura tu acceso a MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # Cambiar por tu clave real
DATABASE = "portout"
USUARIO_MYSQL = "root"

def otorgar_permisos():
    ips = ip_text.get("1.0", tk.END).strip().splitlines()
    
    if not ips:
        messagebox.showwarning("Atención", "No hay IPs ingresadas.")
        return

    otorgadas = []

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DATABASE
        )
        cursor = conn.cursor()

        for ip in ips:
            ip = ip.strip()
            if ip:
                try:
                    query = f"GRANT SELECT, INSERT, UPDATE, DELETE ON portout.* TO '{USUARIO_MYSQL}'@'{ip}';"
                    cursor.execute(query)
                    otorgadas.append(ip)
                    print(f"Permisos otorgados a {ip}")
                except mysql.connector.Error as err:
                    print(f"Error con IP {ip}: {err}")

        cursor.execute("FLUSH PRIVILEGES;")
        conn.commit()
        cursor.close()
        conn.close()

        # Guardar en el archivo
        with open("direccionespermitidas.txt", "a") as f:
            for ip in otorgadas:
                f.write(f"{ip}\n")

        messagebox.showinfo("Éxito", f"Permisos otorgados a {len(otorgadas)} IP(s) y guardadas en direccionespermitidas.txt.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error de MySQL", f"{err}")

# Interfaz gráfica
root = tk.Tk()
root.title("Otorgar permisos por IP - MySQL")

tk.Label(root, text="Ingrese las IPs (una por línea):").pack(pady=5)
ip_text = tk.Text(root, height=10, width=40)
ip_text.pack()

tk.Button(root, text="Otorgar permisos", command=otorgar_permisos).pack(pady=10)

root.mainloop()
