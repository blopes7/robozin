# ############################################################################################################################
#                                                                                                                            #
#                                                                                                                            #
#                               ROBÔ PARA MONITORAR OP. ASSISTIDA v1.4.0 powered by Leandro Freitas                          #
#                                                                                                                            #
#                                                                                                                            #
# ############################################################################################################################

# ... (código anterior)

# Definir as cores do farol
cor_verde = "🟢"
cor_amarelo = "🟡"
cor_vermelho = "🔴"

# Definir os limites para as cores do farol
limite_verde = 0
limite_amarelo = 3
# qualquer coisa diferente é vermelho

# Obter a quantidade da variável 'formatted_result'
# quantidade = int(formatted_result.split(":")[1].split("<br>")[0])
quantidade = int(formatted_result3.split(":")[1].split("<br>")[0].replace('</b> ', ''))

# Escolher a cor do farol com base na quantidade
if quantidade <= limite_verde:
    cor_farol = cor_verde
elif quantidade <= limite_amarelo:
    cor_farol = cor_amarelo
else:
    cor_farol = cor_vermelho

# Formatar o resultado da consulta

# formatted_result2 = ""
# for row in cursor2:
#     formatted_result += f"<b>Total de pedidos Recebidos :</b> {str(row[0][0])}<br><b>Valor total de pedidos Recebidos:</b> {str(row[0][1])}<br><br><b>Total de pedidos Faturados :</b> {str(row[1][0])}<br><b>Valor total de pedidos Faturados:</b> {str(row[1][1])}<br><br>"

formatted_result2 = ""
rows = list(cursor2)

# Primeira linha da matriz
formatted_result2 += f"<b>Total de pedidos Recebidos :</b> {str(rows[0][0])}<br><b>Valor total de pedidos Recebidos:</b> {str(rows[0][1])}<br><br>"

# Segunda linha da matriz
formatted_result2 += f"<b>Total de pedidos Faturados :</b> {str(rows[1][0])}<br><b>Valor total de pedidos Faturados:</b> {str(rows[1][1])}<br><br>"

# Mensagem a ser enviada, neste caso utilizando HTML
message = {
    "cards": [
        {
            "sections": [
                {
                    "widgets": [
                        {
                            "image": {
                                "imageUrl": "https://images2.imgbox.com/62/3b/QJezuElt_o.png"
                            }
                        },
                        {
                            "textParagraph": {
                                "text": f'<b><font color="#00FA9A"><h3>Relatório de Pedidos - {seller}</h3></font>',
                            }
                        },
                    ]
                },
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": f"Informação atualizada dos pedidos até o dia <b>{data_formatada}:"
                            }
                        }
                    ]
                },
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": f"{formatted_result}",
                            }
                        }
                    ]
                },
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": f"{cor_farol} -  {formatted_result3}",
                            }
                        }
                    ]
                },
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": formatted_result2,
                            }
                        }
                    ]
                },
                {
                    "widgets": [

                    ]
                },
                {
                    "widgets": [
                        {
                            "textParagraph": {
                                "text": f'Caso queira ter acesso ao relatorio detalhado dos pedidos, <a href="{planilha}">clique aqui</a>'
                            }
                        }
                    ]

                }
            ]
        }
    ]
}

# ... (código restante)

