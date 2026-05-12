function paginaCadastroReceita(){
    return`
    <div class="container-receita">
    <h1>Cadastro de Receitas</h1>

    <form>
      <div>
        <label>Nome do pagador:</label>
        <input type="text" placeholder="Digite o nome do pagador" id="nome-pagador">
      </div>

      <div>
        <label>CPF/CNPJ do Pagador:</label>
        <input type="text" placeholder="Digite o cpf ou cnpj do pagador" id="cpfcnpj-pagador">
      </div>

      <div>
        <label>Data:</label>
        <input type="text" placeholder="Digite a data do recebimento" id="data-receita">
      </div>

      <div>
        <label>Tipo de Receita:</label>
        <input type="text" placeholder="Produto,serviço,etc..." id="tipo-receita">
      </div>

      <div>
        <label>Valor:</label>
        <input type="text" placeholder="Digite o valor da receita (pagamento)" id="valor-receita">
      </div>

      <div class="btn-area">
        <button type="submit">Cadastrar</button>
      </div>
    </form>

    <div id="footer-cadastroReceita">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
  `
}