import tkinter as tk
from tkinter import messagebox
import sqlite3

class UserProfileApp:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Perfil do Usuário")
        self.root.geometry("400x500")
        self.user_id = user_id
        
        # Cores e estilo
        self.bg_color = "#f0f2f5"
        self.header_color = "#1a73e8"
        self.text_color = "#ffffff"
        self.field_bg = "#ffffff"
        
        self.create_widgets()
        self.load_user_data()
        
    def create_widgets(self):
        # Frame de cabeçalho
        header_frame = tk.Frame(self.root, bg=self.header_color, height=100)
        header_frame.pack(fill=tk.X)
        
        # Título
        tk.Label(header_frame, text="Meu Perfil", font=('Helvetica', 18, 'bold'), 
                bg=self.header_color, fg=self.text_color).pack(pady=20)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Foto de perfil (placeholder)
        self.profile_img = tk.PhotoImage(width=80, height=80)
        profile_label = tk.Label(main_frame, image=self.profile_img, bg=self.bg_color)
        profile_label.pack(pady=10)
        
        # Campos do formulário
        fields = [
            ("Nome:", "name_entry"),
            ("Email:", "email_entry"), 
            ("Curso:", "course_entry"),
            ("Nova Senha:", "password_entry")
        ]
        
        for label_text, var_name in fields:
            frame = tk.Frame(main_frame, bg=self.bg_color)
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label_text, bg=self.bg_color, width=12, anchor='w').pack(side=tk.LEFT)
            
            if "password" in var_name:
                entry = tk.Entry(frame, show="*", bg=self.field_bg)
            else:
                entry = tk.Entry(frame, bg=self.field_bg)
                
            entry.pack(fill=tk.X, expand=True)
            setattr(self, var_name, entry)
        
        # Botões
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(button_frame, text="Salvar Alterações", command=self.save_changes,
                 bg="#1a73e8", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancelar", command=self.root.destroy,
                 bg="#f44336", fg="white", relief=tk.FLAT).pack(side=tk.RIGHT, padx=5)
    
    def load_user_data(self):
        """Carrega os dados do usuário do banco de dados"""
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name, email, course FROM users WHERE id = ?", (self.user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                name, email, course = user_data
                self.name_entry.insert(0, name)
                self.email_entry.insert(0, email)
                self.course_entry.insert(0, course)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os dados: {str(e)}")
        finally:
            conn.close()
    
    def save_changes(self):
        """Salva as alterações no banco de dados"""
        name = self.name_entry.get()
        email = self.email_entry.get()
        course = self.course_entry.get()
        password = self.password_entry.get()
        
        if not name or not email:
            messagebox.showwarning("Aviso", "Nome e email são obrigatórios!")
            return
        
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        
        try:
            if password:
                # Atualiza com senha
                cursor.execute("""
                    UPDATE users 
                    SET name = ?, email = ?, course = ?, password = ?
                    WHERE id = ?
                """, (name, email, course, password, self.user_id))
            else:
                # Atualiza sem alterar senha
                cursor.execute("""
                    UPDATE users 
                    SET name = ?, email = ?, course = ?
                    WHERE id = ?
                """, (name, email, course, self.user_id))
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {str(e)}")
        finally:
            conn.close()

if __name__ == "__main__":
    # Exemplo de uso - substitua 1 pelo ID do usuário real
    root = tk.Tk()
    app = UserProfileApp(root, user_id=1)
    root.mainloop()