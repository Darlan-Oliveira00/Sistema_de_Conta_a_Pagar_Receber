function paginaCadastroFornecedor(){
    return `
        <div class="card-fornecedor">
            <h1>Cadastro de Fornecedor</h1>
            <form>
                <label>Nome Oficial da empresa:</label>
                <input type="text" id="nome-oficial-empresa">
                <br>

                <label>CNPJ:</label>
                <input type="text" id="cnpj" placeholder="00.000.000/0000-00">
                <br>

                <label>E-mail:</label>
                <input type="email" id="email-empresa">
                <br>

                <label>Telefone da Empresa:</label>
                <input type="tel" id="telefone-empresa" placeholder="(00) 00000-0000">
                <br>

                <label>Senha:</label>
                <input type="password" id="senha-empresa">
                <br>

                <label>Confirmar senha:</label>
                <input type="password" id="senha-empresa-cfn">
                <br>

                <button class="btn" type="button" onclick="cadastrarFornecedor()">Cadastre-se</button>
            </form>

            <div class="footer-login">
                <p>Já tem conta? <button id="tela-login" onclick="renderizarPagina('login')">Fazer login</button></p>
            </div>
        </div>
    `
}


async function cadastrarFornecedor() {
    const nome = document.getElementById('nome-oficial-empresa').value.trim();
    const cnpj = document.getElementById('cnpj').value.replace(/\D/g, '');
    const email = document.getElementById('email-empresa').value.trim();
    const telefone = document.getElementById('telefone-empresa').value.replace(/\D/g, '');
    const senha = document.getElementById('senha-empresa').value;
    const confirmarSenha = document.getElementById('senha-empresa-cfn').value;

    if (!nome || !cnpj || !email || !telefone || !senha || !confirmarSenha) {
        alert('Preencha todos os campos obrigatórios');
        return;
    }

    if (cnpj.length !== 14) {
        alert('CNPJ deve ter 14 dígitos');
        return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('E-mail inválido');
        return;
    }

    if (telefone.length < 10) {
        alert('Telefone deve ter no mínimo 10 dígitos');
        return;
    }

    if (senha !== confirmarSenha) {
        alert('As senhas não conferem');
        return;
    }

    if (senha.length < 6) {
        alert('A senha deve ter no mínimo 6 caracteres');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/fornecedor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nome_oficial_empresa: nome,
                cnpj: cnpj,
                email: email,
                numero_telefone_empresa: telefone,
                senha: senha
            })
        });

        const data = await response.json();

        if (!response.ok) {
            const mensagem = data.detail || `Erro ${response.status}: Erro ao cadastrar fornecedor`;
            alert(mensagem);
        }

        alert('Fornecedor cadastrado com sucesso!');
        renderizarPagina('login');

    } catch (error) {
        alert(`${error.message}`);
    }
}