SELECT fatura.idfatura, produtofatura.idproduto, produto.designacao as nomeProduto, produtofatura.quantidade as quantidadeprodutos
FROM fatura 
INNER JOIN produtofatura ON fatura.idfatura = produtofatura.idfatura 
INNER JOIN produto ON produtofatura.idproduto = produto.idproduto