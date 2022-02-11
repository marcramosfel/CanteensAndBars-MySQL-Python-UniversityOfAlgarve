SELECT fatura.idfatura, pratofatura.idprato, prato.nome as nomePrato, pratofatura.quantidade as quantidadepratos
FROM fatura 
INNER JOIN pratofatura ON fatura.idfatura = pratofatura.idfatura 
INNER JOIN prato ON pratofatura.idprato = prato.idprato
