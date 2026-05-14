function paginaCadastroVendas() {
  return `
        <div class="container-vendas">
    <h1>Cadastro de Vendas</h1>

    <form>
      <div>
        <label>CPF/CNPJ do comprador:</label>
        <input type="text" id="cpfcnpj-comprador" placeholder="Digite o cpf ou cnpj do comprador">
      </div>

      <div>
        <label>Forma de pagamento</label>
        <input type="text" id="forma-pagamento" placeholder="Digite a forma de pagamento">
      </div>

      <div>
        <label>Valor da Venda</label>
        <input type="number" id="valor-venda" placeholder="Digite o valor da venda">
      </div>

      <div>
        <label>Porcentagem do desconto</label>
        <input type="number" id="porcentagem" placeholder="Digite a porcentagem d0 desconto">
      </div>

      <div class="btn-area">
        <button type="button" id="btn-cadastroVendas" onclick="cadastrarVendas()" >Cadastrar</button>
      </div>
    </form>
    <div id="footer-cadastroVenda">
      <button onclick="renderizarPagina('layout')" class="btn-voltar">Voltar para dashboard</button>
    </div>
  </div>
    `
}

async function cadastrarVendas() {
  const cpfcnpjComprador = document.getElementById('cpfcnpj-comprador').value.trim();
  const formaPagamento = document.getElementById('forma-pagamento').value.trim();
  const valorVenda = document.getElementById('valor-venda').value.trim();
  const porcentagemDesconto = document.getElementById('porcentagem').value.trim();

  if (!cpfcnpjComprador || !formaPagamento || !valorVenda || !porcentagemDesconto) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  if (isNaN(valorVenda) || isNaN(porcentagemDesconto)) {
    alert('Informe valores numéricos válidos');
    return;
  }

  const valorVendaNum = parseFloat(valorVenda);
  const porcentagemDescontoNum = parseFloat(porcentagemDesconto);

  if (valorVendaNum <= 0 || porcentagemDescontoNum <= 0) {
    alert('Os valores devem ser maiores que zero');
    return;
  }

  try {
    const cpfCnpjVendendor = obterCfpCnpjUsuario();

    const dados = {
      cpf_cnpj_vendendor: cpfCnpjVendendor,
      cpf_cnpj_comprador: cpfcnpjComprador,
      forma_pagamento: formaPagamento,
      valor_venda: valorVendaNum,
      porcentagem_desconto: porcentagemDescontoNum
    };

    const btnCadastroVendas = document.getElementById('btn-cadastroVendas');
    btnCadastroVendas.disabled = true;
    btnCadastroVendas.textContent = "Cadastrando...";

    const response = await fetch(`${API_BASE_URL}/vendas`, {
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
    const btnCadastroVendas = document.getElementById('btn-cadastroVendas');
    btnCadastroVendas.disabled = false;
    btnCadastroVendas.textContent = "Cadastrar";
  }
}