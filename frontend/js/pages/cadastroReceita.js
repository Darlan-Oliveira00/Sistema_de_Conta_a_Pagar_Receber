function paginaCadastroReceita() {
  return `
    <div class="container-receita">
    <h1>Cadastro de Receitas</h1>

    <form>
      <div>
        <label>CPF/CNPJ do Pagador:</label>
        <input type="text" placeholder="Digite o cpf ou cnpj do pagador" id="cpfcnpj-pagador-receita">
      </div>

      <div>
        <label>Data:</label>
        <input type="date" placeholder="Digite a data do recebimento" id="data-receita">
      </div>

      <div>
        <label>Tipo de Receita:</label>
        <input type="text" placeholder="Produto,serviço,etc..." id="tipo-receita">
      </div>

      <div>
        <label>Valor:</label>
        <input type="number" placeholder="Digite o valor da receita (pagamento)" id="valor-receita">
      </div>

      <div class="btn-area">
        <button type="button" id="btn-cadastroReceita" onclick="cadastrarReceita()">Cadastrar</button>
      </div>
    </form>

    <div id="footer-cadastroReceita">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
  `
}

async function cadastrarReceita() {
  const cpfcnpjPagadorReceita = document.getElementById('cpfcnpj-pagador-receita').value.trim();
  const valorReceita = document.getElementById('valor-receita').value.trim();
  const dataReceita = document.getElementById('data-receita').value.trim();
  const origemReceita = document.getElementById('tipo-receita').value.trim();

  if (!cpfcnpjPagadorReceita || !valorReceita || !dataReceita || !origemReceita) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  if (isNaN(valorReceita)) {
    alert('Informe valores numéricos válidos');
    return;
  }

  const valorReceitaNum = parseFloat(valorReceita);

  if (valorReceitaNum <= 0) {
    alert('Os valores devem ser maiores que zero');
    return;
  }

  try {
    const cpfcnpjRecebedorReceita = obterCfpCnpjUsuario();

    const dados = {
      cpf_cnpj_recebedor: cpfcnpjRecebedorReceita,
      cpf_cnpj_pagado: cpfcnpjPagadorReceita,
      valor_receita: valorReceita,
      data_evento_receita: dataReceita,
      origem_receita: origemReceita
    };

    const btnCadastroReceita = document.getElementById('btn-cadastroReceita');
    btnCadastroReceita.disabled = true;
    btnCadastroReceita.textContent = "Cadastrando...";

    const response = await fetch(`${API_BASE_URL}/receita`, {
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
  } finally {
    const btnCadastroReceita = document.getElementById('btn-cadastroReceita');
    btnCadastroReceita.disabled = false;
    btnCadastroReceita.textContent = "Cadastrar";
  }
}