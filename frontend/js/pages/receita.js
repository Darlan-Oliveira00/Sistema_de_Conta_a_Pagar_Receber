function paginaReceitas(){
    return `
        <div class="card-receita">
                <h1>Contas a Receber</h1>

                <div class="top-bar">
                    <button class="btn-cadastrar-receita" id="cadastrar-receita" onclick="renderizarPagina('cadastroReceita')">Cadastrar Receita</button>

                    <input
                        type="text"
                        placeholder="Buscar Receita"
                        class="search"
                        id="buscar-receita"
                        onkeyup="pesquisarReceita()"
                    >
                </div>

                <div class="table-container">
                    <table id="tabela-receitas">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>CPF/CNPJ</th>
                                <th>Data</th>
                                <th>Tipo</th>
                                <th>Valor</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td>Fulano</td>
                                <td>123.123.123-00</td>
                                <td>26/04/2026</td>
                                <td>Recorrente</td>
                                <td>R$ 200,00</td>
                            </tr>

                            <tr>
                                <td>Mercado Central</td>
                                <td>12.345.678/0001-00</td>
                                <td>10/05/2026</td>
                                <td>Fixa</td>
                                <td>R$ 450,00</td>
                            </tr>

                            <tr>
                                <td>Internet</td>
                                <td>98.765.432/0001-00</td>
                                <td>15/05/2026</td>
                                <td>Mensal</td>
                                <td>R$ 120,00</td>
                            </tr>

                            <tr>
                                <td>Energia</td>
                                <td>11.222.333/0001-99</td>
                                <td>18/05/2026</td>
                                <td>Mensal</td>
                                <td>R$ 320,00</td>
                            </tr>

                            <tr>
                                <td>Fornecedor XP</td>
                                <td>55.444.222/0001-10</td>
                                <td>20/05/2026</td>
                                <td>Única</td>
                                <td>R$ 950,00</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
    `
}

function pesquisarReceita() {
    const input = document.getElementById('buscar-receita');
    const filtro = input.value.toUpperCase();
    const tabela = document.getElementById('tabela-receitas');
    const linhas = tabela.querySelectorAll('tbody tr');

    for (let i = 0; i < linhas.length; i++) {
        const nome = linhas[i].getElementsByTagName('td')[0].textContent;
        const cpfCnpj = linhas[i].getElementsByTagName('td')[1].textContent;
        const data = linhas[i].getElementsByTagName('td')[2].textContent;
        const tipo = linhas[i].getElementsByTagName('td')[3].textContent;

        if (nome.toUpperCase().includes(filtro) || 
            cpfCnpj.toUpperCase().includes(filtro) ||
            tipo.toUpperCase().includes(filtro)) {
            linhas[i].style.display = '';
        } else {
            linhas[i].style.display = 'none';
        }
    }
}