function paginaLogin() {
    return `
    <div class="container">
        <div id="login" class="section active">
            <div class="login-form">
                <div class="login-header">
                    <img src="./imgs/icons/logo.png" alt="logo">
                    <h1>BEM-VINDO!</h1>
                    <p>Faça login para acessar sua conta</p>
                </div>

                <form id="systemform">
                    <div class="form-group">
                        <label for="tipoUsuario">Tipo de Usuário:</label>
                        <select id="tipoUsuario" onchange="mudarTipoUsuario()">
                            <option value="cliente">Cliente (CPF)</option>
                            <option value="fornecedor">Fornecedor (CNPJ)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="usuario">CPF/CNPJ:</label>
                        <input type="text" name="usuario" id="usuario" placeholder="Digite seu CPF" maxlength="14">
                    </div>

                    <div class="form-group">
                        <label for="senha">Senha:</label>
                        <input type="password" name="senha" id="senha" placeholder="Digite sua senha">
                    </div>

                    <div class="btn-entrar">
                        <button type="button" onclick="fazerLogin()">Entrar</button>
                    </div>
                </form>

                <div id="logout">
                    <p>Ainda não tem conta? <button type="button" onclick="abrirCadastroCliente()"><b>Cadastre-se cliente</b></button></p>
                    <p>Ainda não tem conta? <button type="button" onclick="abrirCadastroFornecedor()"><b>Cadastre-se fornecedor</b></button></p>
                </div>
            </div>
        </div>
    </div>
    `;
}

// Mudar placeholder e máximo de caracteres conforme tipo
function mudarTipoUsuario() {
    const tipoUsuario = document.getElementById('tipoUsuario').value;
    const inputUsuario = document.getElementById('usuario');

    if (tipoUsuario === 'cliente') {
        inputUsuario.placeholder = 'Digite seu CPF (11 dígitos)';
        inputUsuario.maxLength = '11';
    } else {
        inputUsuario.placeholder = 'Digite seu CNPJ (14 dígitos)';
        inputUsuario.maxLength = '14';
    }

    // Limpar o campo ao trocar de tipo
    inputUsuario.value = '';
}

async function fazerLogin() {
    const tipoUsuario = document.getElementById('tipoUsuario').value;
    const cpfCnpj = document.getElementById('usuario').value.replace(/\D/g, '');
    const senha = document.getElementById('senha').value;

    // Validações
    if (!cpfCnpj || !senha) {
        alert('Preencha todos os campos');
        return;
    }

    if (tipoUsuario === 'cliente' && cpfCnpj.length !== 11) {
        alert('CPF deve ter 11 dígitos');
        return;
    }

    if (tipoUsuario === 'fornecedor' && cpfCnpj.length !== 14) {
        alert('CNPJ deve ter 14 dígitos');
        return;
    }

    try {
        // Escolher rota conforme tipo de usuário
        const rota = tipoUsuario === 'cliente' ? '/login_cliente' : '/login_fornecedor/';

        const response = await fetch(`${API_BASE_URL}${rota}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                cpf: cpfCnpj,  // Para cliente
                cnpj: cpfCnpj,  // Para fornecedor
                senha 
            })
        });

        if (response.ok) {
            // const usuario = await response.json();
            console.log('Login bem-sucedido!', usuario);

            // ✅ Salvar dados do usuário no localStorage
            localStorage.setItem('usuario', JSON.stringify(cpfCnpj));
            localStorage.setItem('tipoUsuario', tipoUsuario);

            renderizarLayout();
        } else if (response.status === 404) {
            const erro = await response.json();
            alert('Erro: ' + erro.detail);
            console.error('Usuário não encontrado');
        } else if (response.status === 401) {
            const erro = await response.json();
            alert('Erro: ' + erro.detail);
        } else {
            alert('Erro ao fazer login');
            console.error('Falha no login');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Erro ao conectar com o servidor');
    }
}

function abrirCadastroCliente() {
    renderizarPagina('cadastroCliente');
}

function abrirCadastroFornecedor(){
    renderizarPagina('cadastroFornecedor');
}