function paginaCadastroDespesa(){
    return`
        <div class="container-despesa">
    <h1>Cadastro de Despesas</h1>

    <form>
      <div>
        <label>CPF/CNPJ do Recebedor:</label>
        <input type="text" placeholder="Digite o cpf ou cnpj do recebedor" id="cpf/cnpj-recebedor">
      </div>

      <div>
        <label>Data:</label>
        <input type="date" id="data-despesa">
      </div>

      <div>
        <label>Tipo de Despesa:</label>
        <select>
            <option value="">Selecione uma opção</option>
            <option value="recorrente">Recorrente</option>
            <option value="extraordinaria">Extraordinaria</option>
        </select>
      </div>

      <div>
        <label>Valor:</label>
        <input type="number" placeholder="Digite o valor da despesa (pagamento)" id="valor-despesa">
      </div>

      <div>
        <label>Descrição:</label>
        <input type="text" placeholder="Digite a descrição da despesa" id="descricao-despesa">
      </div>

      <div class="btn-area">
        <button type="submit">Cadastrar</button>
      </div>
    </form>

    <div id="footer-cadastroDespesa">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
    `
}