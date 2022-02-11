SELECT 
	idf,
    SUM(subtotal) as total
FROM
    ((SELECT 
        produtofatura.idfatura AS idf,
            produtofatura.idproduto AS id_item,
            produtofatura.quantidade AS qtd,
            produtofatura.idespacoAlimentar AS espali,
            produtoespacoalimentar.preco AS preco,
            (produtoespacoalimentar.preco *  produtofatura.quantidade) as subtotal,
            'produto'
    FROM
        barcantina.produtofatura
    INNER JOIN produtoespacoalimentar ON produtofatura.idproduto = produtoespacoalimentar.idproduto
        AND produtofatura.idespacoAlimentar = produtoespacoalimentar.idespacoAlimentar
    INNER JOIN fatura ON fatura.idfatura = produtofatura.idfatura) UNION (SELECT 
        pratofatura.idfatura AS idf,
            pratofatura.idprato AS id_item,
            pratofatura.quantidade AS qtd,
            pratofatura.idespacoAlimentar AS espali,
            pratoespacoalimentar.preco AS preco,
            (pratoespacoalimentar.preco * pratofatura.quantidade) as subtotal,
            
            'prato'
    FROM
        barcantina.pratofatura
    INNER JOIN pratoespacoalimentar ON pratofatura.idprato = pratoespacoalimentar.idprato
        AND pratofatura.idespacoAlimentar = pratoespacoalimentar.idespacoAlimentar
    INNER JOIN fatura ON fatura.idfatura = pratofatura.idfatura)
    ) AS faturaglobal
    where idf = 32
	
    ORDER BY idf