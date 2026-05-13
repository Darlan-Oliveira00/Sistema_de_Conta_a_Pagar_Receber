function paginaCadastroVendas(){
    return`
        <div class="container-vendas">
    <h1>Cadastro de Vendas</h1>

    <form>
      <div>
        <label>Nome do produto:</label>
        <input type="text" placeholder="Digite o nome do produto">
      </div>

      <div>
        <label>CPF/CNPJ do comprador:</label>
        <input type="text" placeholder="Digite o cpf ou cnpj do comprador">
      </div>

      <div>
        <label>Forma de pagamento</label>
        <input type="text" placeholder="Digite a data do pagamento">
      </div>

      <div>
        <label>Porcentagem do desconto</label>
        <input type="text" placeholder="Digite a porcentagem de desconto">
      </div>

      <div>
        <label>data do pagamento:</label>
        <input type="text" placeholder="Digite o valor do pagamento">
      </div>

      <div class="btn-area">
        <button type="submit">Cadastrar</button>
      </div>
    </form>
    <div id="footer-cadastroVenda">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
    `
}