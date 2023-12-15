import requests
import json
import html
import openpyxl
import pyodbc
from datetime import datetime
import locale
from datetime import date
import calendar
from html import escape
import pandas as pd

locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# ...

# Lista de gercreds
gercreds = ['gercred001', 'gercred002', 'gercred003', 'gercred004', 'gercred005']

# Dicionário de webhooks correspondentes aos gercreds
webhooks = {
    'gercred001': 'URL_WEBHOOK_001',
    'gercred002': 'URL_WEBHOOK_002',
    'gercred003': 'URL_WEBHOOK_003',
    'gercred004': 'URL_WEBHOOK_004',
    'gercred005': 'URL_WEBHOOK_005',
}

for gercred in gercreds:
    # ...

    # Substituir 'GERCRED40' pela variável gercred
    result1 = """
    DECLARE @AgreementName VARCHAR(12) = '{}'
    DECLARE @DataInicio VARCHAR(16) = '{}'
    select 
    count(1) as 'Quantidade',
    case 
    when SUM(Amount) is null then 'Sem pedidos pendentes'
    else FORMAT(SUM(Amount) ,'c', 'pt-br') 
    end as "valor"
    from VW_Authorization va1 with (nolock) where AuthorizationId in 
    (
    select va.AuthorizationId from VW_Authorization va 
    where 1=1
    AND va.AgreementName = '{}'
    and va.SellerId = @AgreementName
    EXCEPT 
    select AuthorizationId from Invoices i with (nolock)
    where 1=1
    AND i.AgreementName = '{}'
    and i.ProcessResult  = 1
    and i.SellerName = @AgreementName
    )
    and va1.AuthorizationResult  = 'Approved'
    and va1.CreatedAt > @DataInicio
    """.format(gercred, DataInicio, gercred, gercred)

    # ...

    # Substituir 'GERCRED40' pela variável gercred
    result2 = """
    DECLARE @AgreementName VARCHAR(12) = '{}'
    DECLARE @DataInicio VARCHAR(16) = '{}'
        SELECT COUNT(va.AuthorizationId), 
        case 
    when SUM(Amount) is null then 'Sem pedidos'
    else FORMAT(SUM(Amount) ,'c', 'pt-br')
    end as 'Valor'
         FROM VW_Authorization va WITH (NOLOCK)
         WHERE CreditReasonId = 1
         AND va.AgreementName ='{}'
         AND va.SellerId = @AgreementName
         AND va.CreatedAt > @DataInicio 
         union all 
    SELECT COUNT(va.Id), 
    case 
    when SUM(Amount) is null then 'Sem Faturamentos '
    else FORMAT(SUM(Amount) ,'c', 'pt-br')   
    end as 'Valor'
         FROM Invoices VA WITH (NOLOCK)
         WHERE ProcessResult = 1
         AND va.sellerName = @AgreementName
         AND va.AgreementName ='{}'
         AND va.CreatedAt > @DataInicio
    """.format(gercred, DataInicio, gercred, gercred)

    # ...

    # Substituir 'GERCRED40' pela variável gercred
    sql_query = """
    DECLARE @AgreementName VARCHAR(12) = '{}'
    DECLARE @DataInicio VARCHAR(16) = '{}'
    SELECT 'Pedidos Não Recebidos' as 'Tipo',
           document as 'CNPJ Cliente',
           '-' as 'CNPJ Emissor',
           Format(amount, 'c', 'pt-br'),
           referencecode as 'Numero do Pedido',
           '-'                             AS 'Numero Nota fiscal',
           createdat as 'Data de criação',
           CONVERT(VARCHAR, expiresat, 20) AS 'DATA EXPIRAÇÃO'
    FROM   vw_authorization va1
    WHERE  authorizationid IN (SELECT va.authorizationid
                               FROM   vw_authorization va
                               WHERE  sellerid = @AgreementName
                               EXCEPT
                               SELECT authorizationid
                               FROM   invoices i WITH (nolock)
                               WHERE  i.sellername = @AgreementName
                                      AND i.processresult = 1)
           AND va1.authorizationresult = 'Approved'
           AND va1.agreementname = '{}'
           AND va1.createdat > @DataInicio
    UNION ALL
    SELECT 'Pedidos'                       AS 'Tipo',
           document                        AS 'CNPJ Cliente',
           '-',
           Format(amount, 'c', 'pt-br')    AS 'Valor',
           referencecode                   AS 'Numero do Pedido',
           '-'                             AS 'Numero Nota fiscal',
           createdat                       AS 'Data de criação',
           CONVERT(VARCHAR, expiresat, 20) AS 'Data Expiração'
    FROM   vw_authorization va WITH (nolock)
    WHERE  creditreasonid = 1
           AND va.agreementname = '{}'
           AND va.sellerid = @AgreementName
           AND va.createdat > @DataInicio
    UNION ALL
    SELECT 'Operações',
           i.receiverdocument             AS 'CNPJ Cliente',
           CONVERT(VARCHAR, i.IssuerDocument, 20)			  as 'CNPJ Emissor',
           Format(i.amount, 'c', 'pt-br') AS 'Valor',
           va2.referencecode,
           i.number                       AS 'Numero da Nota',
           i.createdat                    AS 'Data de criação',
           '-'
    FROM   invoices i WITH (nolock),
           vw_authorization va2
    WHERE  i.authorizationid = va2.authorizationid
           AND i.processresult = 1
           AND i.sellername = @AgreementName
           AND i.createdat > @DataInicio
           AND i.agreementname = '{}'
    """.format(gercred, DataInicio, gercred)

    # ...

    # Substituir 'GERCRED40' pela variável gercred
    resultPend1 = """
    DECLARE @AgreementName VARCHAR(12) = '{}'
    select 
     count(1) as 'Quantidade'
    from VW_Authorization va1 with (nolock) where AuthorizationId in 
    (
    select va.AuthorizationId from VW_Authorization va 
    where 1=1
    AND va.AgreementName ='{}'
    and va.SellerId = @AgreementName
    EXCEPT 
    select AuthorizationId from Invoices i with (nolock)
    where 1=1
    AND i.AgreementName ='{}'
    and i.ProcessResult 
