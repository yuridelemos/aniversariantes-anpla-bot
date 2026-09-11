from email.utils import formataddr
import os
import smtplib
from email.mime.text import MIMEText


def montar_mensagem(aniversariantes_df, hoje):
    linhas = ""

    for _, row in aniversariantes_df.iterrows():
        linhas += f"""
        <tr>
            <td style="
                padding: 10px 12px;
                border-bottom: 1px solid #e5e5e5;
            ">
                {row["Nome"]}
            </td>

            <td style="
                padding: 10px 12px;
                border-bottom: 1px solid #e5e5e5;
                text-align: center;
            ">
                {row["Data de Nascimento"].strftime("%d/%m/%Y")}
            </td>

            <td style="
                padding: 10px 12px;
                border-bottom: 1px solid #e5e5e5;
                text-align: center;
            ">
                {row["Idade"]} anos
            </td>

            <td style="
                padding: 10px 12px;
                border-bottom: 1px solid #e5e5e5;
            ">
                {row["Ramo"]}
            </td>

            <td style="
                padding: 10px 12px;
                border-bottom: 1px solid #e5e5e5;
            ">
                {row["Observacao"]}
            </td>
        </tr>
        """

    return f"""
    <html>
        <body style="
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            font-family: Arial, Helvetica, sans-serif;
            color: #333333;
        ">

            <div style="
                max-width: 1000px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 8px;
            ">

                <h2 style="
                    margin: 0 0 5px 0;
                    color: #333333;
                ">
                    🎂 Aniversariantes do Dia
                </h2>

                <p style="
                    margin: 0 0 25px 0;
                    color: #666666;
                    font-size: 15px;
                ">
                    {hoje.strftime("%d/%m/%Y")}
                </p>

                <p style="
                    margin-bottom: 20px;
                    font-size: 15px;
                ">
                    Confira abaixo os aniversariantes de hoje:
                </p>

                <table style="
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                ">

                    <thead>
                        <tr style="
                            background-color: #f2f2f2;
                        ">

                            <th style="
                                padding: 12px;
                                text-align: left;
                                border-bottom: 2px solid #d9d9d9;
                            ">
                                Nome
                            </th>

                            <th style="
                                padding: 12px;
                                text-align: center;
                                border-bottom: 2px solid #d9d9d9;
                            ">
                                Nascimento
                            </th>

                            <th style="
                                padding: 12px;
                                text-align: center;
                                border-bottom: 2px solid #d9d9d9;
                            ">
                                Idade
                            </th>

                            <th style="
                                padding: 12px;
                                text-align: left;
                                border-bottom: 2px solid #d9d9d9;
                            ">
                                Ramo
                            </th>

                            <th style="
                                padding: 12px;
                                text-align: left;
                                border-bottom: 2px solid #d9d9d9;
                            ">
                                Observação
                            </th>

                        </tr>
                    </thead>

                    <tbody>
                        {linhas}
                    </tbody>

                </table>

                <p style="
                    margin-top: 25px;
                    margin-bottom: 0;
                    font-size: 15px;
                ">
                    🎉 Deseje parabéns a todos!
                </p>

            </div>

        </body>
    </html>
    """


def enviar_email_aniversariantes(aniversariantes_df, hoje):
    if aniversariantes_df.empty:
        print("Nenhum aniversariante hoje, e-mail não enviado.")
        return

    mensagem = montar_mensagem(aniversariantes_df, hoje)

    msg = MIMEText(mensagem, "html", "utf-8")

    msg["Subject"] = (
        f"Aniversariante(s) do dia {hoje.strftime('%d/%m/%Y')}"
    )

    msg["From"] = formataddr(
        ("Aniversariantes do Dia", os.getenv("EMAIL_USER"))
    )

    msg["To"] = os.getenv("EMAIL_ANPLA")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASSWORD")
        )

        smtp.send_message(msg)

    print("E-mail enviado com sucesso!")