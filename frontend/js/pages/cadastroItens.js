function paginaCadastroItens(){
    return`
        <div class="container-item">
    <h1>Cadastro de itens</h1>

    <form>
      <div>
        <label>Tipo de item</label>
        <input type="text" placeholder="Produto/Serviço">
      </div>

      <div>
        <label>Descrição do item:</label>
        <input type="text" placeholder="informe a descrição do item">
      </div>

      <div>
        <label>Nome do item:</label>
        <input type="text" placeholder="informe o nome do item">
      </div>

      <div>
        <label>Valor Bruto:</label>
        <input type="text" placeholder="informe o valor bruto">
      </div>

      <div>
        <label>Valor final:</label>
        <input type="text" placeholder="Digite o valor final">
      </div>

      <div class="btn-area">
        <button type="submit">Cadastrar</button>
      </div>
    </form>
    <div id="footer-cadastroItens">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
    `
}