import os
import smtplib
from email.mime.text import MIMEText


def montar_mensagem(aniversariantes_df, hoje):
    linhas = [
        f'{row["Nome"]} - {row["Data de Nascimento"].strftime("%d/%m/%Y")} - {row["Idade"]} anos'
        for _, row in aniversariantes_df.iterrows()
    ]
    return (
        f"🎂 Aniversariantes do dia {hoje.strftime('%d/%m/%Y')}\n\n"
        + "\n".join(linhas)
        + "\n\nDeseje parabéns a todos!"
    )


def enviar_email_aniversariantes(aniversariantes_df, hoje):
    if aniversariantes_df.empty:
        print("Nenhum aniversariante hoje, e-mail não enviado.")
        return

    mensagem = montar_mensagem(aniversariantes_df, hoje)

    msg = MIMEText(mensagem)
    msg["Subject"] = f"Aniversariante(s) do dia {hoje.strftime('%d/%m/%Y')}"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_ANPLA")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

    print("E-mail enviado com sucesso!")