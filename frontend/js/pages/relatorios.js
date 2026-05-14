function paginaRelatorio(){
    return`
        <div class="card-relatorios">
    <h2>Relatorios</h2>

    <button class="btn">Gerar Relatorio PDF</button>

    <button class="btn">Gerar Relatorio XLS</button>

    <button class="btn">Gerar Relatorio XML</button>
  </div>
    `
}

// async function gerarRelatorio(tipo) {
//   try {
//     const rota = obterTipoUsuario();
//     const cpfCnpj = obterCfpCnpjUsuario();

//     if (!cpfCnpj) {
//       alert('Erro: CPF/CNPJ não encontrado');
//       return;
//     }

//     const btn = event.target;
//     btn.disabled = true;
//     btn.textContent = 'Gerando...';

//     const response = await fetch(`${API_BASE_URL}/relatorio/${tipo}/${rota}`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ cpf_cnpj: cpfCnpj })
//     });

//     if (response.ok) {
//       // Obter o blob do arquivo
//       const blob = await response.blob();
      
//       // Criar URL temporária
//       const url = window.URL.createObjectURL(blob);
      
//       // Criar link de download
//       const link = document.createElement('a');
//       link.href = url;
//       link.download = `relatorio_${new Date().getTime()}.${tipo}`;
      
//       // Disparar download
//       document.body.appendChild(link);
//       link.click();
//       document.body.removeChild(link);
      
//       // Liberar memória
//       window.URL.revokeObjectURL(url);
      
//       alert('Relatório gerado com sucesso!');
//     } else {
//       const erro = await response.json();
//       alert(`Erro: ${erro.detail || 'Erro ao gerar relatório'}`);
//     }

//   } catch (error) {
//     console.error('Erro:', error);
//     alert(`Erro ao gerar relatório: ${error.message}`);
//   } finally {
//     const btn = event.target;
//     btn.disabled = false;
//     btn.textContent = `Gerar Relatório ${tipo.toUpperCase()}`;
//   }
// }