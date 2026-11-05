# Cineluvra — atualizações Android

Repositório público de distribuição e atualização do **Cineluvra**, criado por Denny Ximenes.

> **Aviso de estabilidade (05/11/2026):** o APK **1.1.1** foi publicado com uma tabela de strings DEX inválida e pode não iniciar. Não instale a 1.1.1. A correção **1.1.2** (versionCode 5) deve ser testada em um aparelho antes da publicação da Release. O validador agora bloqueia DEX fora da ordem exigida e identifica corretamente o certificado exibido pelo apksigner. Não desinstale o aplicativo para evitar perda de dados locais.

- Aplicativo Android: `br.com.dennyximenes.cineluvra`
- Certificado original esperado (SHA-256): `269da380880d92774b52213e3621c3927a222eb2593c6360bfc07de493066568`
- Versão inicial: **1.1.1**, `versionCode 4`
- Manifesto após a publicação válida: [update.json](https://raw.githubusercontent.com/SrDanvers/cineluvra-atualizacoes/main/update.json)

## Alternativa simples: publicador para Windows

O **Publicador Automático GitHub** distribuído com o APK oficial contém `PUBLICAR_CINELUVRA.bat` e `Publicar-Cineluvra.ps1`. Execute o arquivo BAT no computador Windows, autorize o GitHub CLI pelo navegador apenas na primeira vez e o script criará a Release com o APK, usando a conta `SrDanvers`. A publicação dispara o workflow deste repositório.

O publicador não guarda credenciais nem publica chaves privadas. Para novos APKs, é necessário manter o pacote, o certificado e aumentar o versionCode. O envio pela integração do ChatGPT não suporta atualmente anexar arquivos binários a Releases, por isso o publicador usa autenticação local segura.

## Publicar correção de inicialização (1.1.2)

Use o pacote de publicação corrigido, contendo `Cineluvra-1.1.2.apk`, primeiro para atualizar e testar o celular, depois para criar a Release `v1.1.2` pelo GitHub CLI. **Não execute novamente o workflow da v1.1.1**, porque essa versão contém código DEX inválido e será rejeitada.

## Publicar a histórica 1.1.1 (não instalar)

1. Baixe o APK oficial `Cineluvra-1.1.1.apk` da conversa com o desenvolvedor.
2. Abra [Nova Release](https://github.com/SrDanvers/cineluvra-atualizacoes/releases/new).
3. Crie a tag `v1.1.1`, com título `Cineluvra 1.1.1`.
4. Anexe **somente o arquivo `Cineluvra-1.1.1.apk`**, escreva as notas e clique em **Publish release**. Não anexe ZIP do projeto.
5. Abra [Actions](https://github.com/SrDanvers/cineluvra-atualizacoes/actions), escolha `Publicar atualização Cineluvra` e confira se o processo terminou com sucesso.
6. Confirme que [update.json](https://raw.githubusercontent.com/SrDanvers/cineluvra-atualizacoes/main/update.json) foi criado e contém `latestVersionName: "1.1.1"`, `latestVersionCode: 4`, URL e SHA-256.
7. Se o workflow falhar ao fazer push, confira `Settings > Actions > General > Workflow permissions`, permitindo `Read and write permissions` e regras de proteção da branch.

## Próximas versões

Para publicar `v1.1.2`, gere o APK `Cineluvra-1.1.2.apk` com `versionCode 5`, **mesmo identificador do aplicativo e mesma assinatura original**; crie uma nova Release com esse APK. O workflow valida o APK e publica automaticamente o manifesto. Não reenvie um APK modificado com o mesmo `versionCode`.

O aplicativo 1.1.1 consulta o manifesto quando a verificação é acionada. Uma versão com código maior exibe aviso para baixar a atualização e abrir a instalação usando o Android, sempre com confirmação do usuário.

## Proteção do projeto

**Nunca publique** chaves `.p12`, `.jks`, senhas, tokens, arquivos privados do Android Studio ou backups pessoais. Os únicos arquivos necessários no repositório público são o workflow, validador, README, notas e o `update.json` gerado após uma Release. O APK é anexado à Release, e não enviado ao código-fonte.

### Limitações

- O GitHub gera o manifesto; a instalação do APK exige confirmação do Android.
- O hash SHA-256 é gerado no workflow, mas a versão 1.1.1 ainda não confere localmente o hash do arquivo baixado pelo navegador.
- A atualização do catálogo de filmes e séries exige gerar um novo APK.
- A primeira Release ainda precisa ser publicada antes de afirmar que o fluxo ponta a ponta funciona.
