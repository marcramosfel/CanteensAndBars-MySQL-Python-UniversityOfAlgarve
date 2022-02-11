SELECT fatura.idfatura, pratofatura.idprato, prato.nome as nomePrato, pratofatura.quantidade as quantidadepratos,
 produtofatura.idproduto , produto.designacao as nomeProduto , produto.consumivel, produtofatura.quantidade as quantidadeprodutos  FROM fatura 
INNER JOIN pratofatura ON fatura.idfatura = pratofatura.idfatura
INNER JOIN produtofatura ON pratofatura.idfatura = produtofatura.idfatura 
INNER JOIN prato ON pratofatura.idprato = prato.idprato
INNER JOIN produto ON produtofatura.idproduto = produto.idproduto

order by idfatura