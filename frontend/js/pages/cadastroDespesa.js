function paginaCadastroDespesa() {
  return `
        <div class="container-despesa">
    <h1>Cadastro de Despesas</h1>

    <form>
      <div>
        <label>CPF/CNPJ do Recebedor:</label>
        <input type="text" placeholder="Digite o cpf ou cnpj do recebedor" id="cpfcnpj-recebedor">
      </div>

      <div>
        <label>Data:</label>
        <input type="date" id="data-despesa">
      </div>

      <div>
        <label>Tipo de Despesa:</label>
        <select id="tipo-despesa">
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
        <button type="button" id="btn-cadastroDespesa" onclick="cadastrarDespesa()" >Cadastrar</button>
      </div>
    </form>

    <div id="footer-cadastroDespesa">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
    `
}

async function cadastrarDespesa() {
  const cpfcnpjPagador = obterCfpCnpjUsuario();
  const cpfcnpjRecebedor = document.getElementById('cpfcnpj-recebedor').value.trim().replace(/\D/g, '');
  const data = document.getElementById('data-despesa').value.trim();
  const tipo = document.getElementById('tipo-despesa').value.trim();
  const valor = document.getElementById('valor-despesa').value.trim();

  if (!cpfcnpjRecebedor || !data || !tipo || !valor) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  if (tipo != 'recorrente' && tipo != 'extraordinaria'){
    alert('Tipo de despesa invalido');
  }

  if (isNaN(valor)) {
    alert('Informe valores numéricos válidos');
    return;
  }

  const valorNum = parseFloat(valor);

  if (valorNum <= 0) {
    alert('O valor deve ser maior que zero');
    return;
  }

  try {

    const dados = {
      cpf_cnpj_pagador: cpfcnpjPagador,
      cpf_cnpj_recebedor: cpfcnpjRecebedor,
      tipo_de_despesa: tipo,
      valor_despesas: valorNum,
      data_evento: data
    };

    const btnCadastroDespesa = document.getElementById('btn-cadastroDespesa');
    btnCadastroDespesa.disabled = true;
    btnCadastroDespesa.textContent = "Cadastrando...";

    const response = await fetch(`${API_BASE_URL}/despesas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dados)
    });

    if (response.ok) {
      const item = await response.json();

      alert(`Item "${nome}" cadastrado com sucesso!`);

    } else {
      const erro = await response.json();
      alert(`Erro ao cadastrar: ${erro.detail || 'Erro desconhecido'}`);
    }

  } catch (error) {
    alert(`Erro ao conectar ao servidor: ${error.message}`);
  }finally{
    const btnCadastroDespesa = document.getElementById('btn-cadastroDespesa');
    btnCadastroDespesa.disabled = false;
    btnCadastroDespesa.textContent = "Cadastrar";
  }
}