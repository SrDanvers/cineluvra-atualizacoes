# Cineluvra — atualizações Android

Repositório público de distribuição e atualização do **Cineluvra**, criado por Denny Ximenes.

> **Aviso de estabilidade (05/11/2026):** as versões **1.1.1 e 1.1.2** apresentaram falhas de inicialização. **Não instale nem republique essas versões.** A versão **1.1.3** foi confirmada pelo usuário como capaz de iniciar novamente. A publicação da Release 1.1.3 ainda precisa ser concluída, assim como os testes de reprodução no aparelho. O validador bloqueia versionCode abaixo de 6 e alterações no DEX nativo sem revisão. Preserve os dados do aplicativo.

- Aplicativo Android: `br.com.dennyximenes.cineluvra`
- Certificado original esperado (SHA-256): `269da380880d92774b52213e3621c3927a222eb2593c6360bfc07de493066568`
- Próxima versão a publicar: **1.1.3**, `versionCode 6`
- Manifesto após a publicação válida: [update.json](https://raw.githubusercontent.com/SrDanvers/cineluvra-atualizacoes/main/update.json)

## Alternativa simples: publicador para Windows

O **Publicador Automático GitHub** distribuído com o APK oficial contém `PUBLICAR_CINELUVRA.bat` e `Publicar-Cineluvra.ps1`. Execute o arquivo BAT no computador Windows, autorize o GitHub CLI pelo navegador apenas na primeira vez e o script criará a Release com o APK, usando a conta `SrDanvers`. A publicação dispara o workflow deste repositório.

O publicador não guarda credenciais nem publica chaves privadas. Para novos APKs, é necessário manter o pacote, o certificado e aumentar o versionCode. O envio pela integração do ChatGPT não suporta atualmente anexar arquivos binários a Releases, por isso o publicador usa autenticação local segura.

## Publicar recuperação estável de inicialização (1.1.3)

Utilize o pacote `Cineluvra_Publicador_1_1_3_GitHub.zip` com `Cineluvra-1.1.3.apk`. O aplicativo já teve a abertura confirmada no celular. Execute o `PUBLICAR_CINELUVRA.bat` no Windows para criar a Release `v1.1.3`. O workflow validará o APK e criará o `update.json`. Não publique as versões 1.1.1 ou 1.1.2, que apresentam falhas.

## Registro da versão 1.1.1 (não instalar)

A Release `v1.1.1` permanece como registro histórico, mas não é recomendada. O workflow original falhou, e não foi criado `update.json`. O novo validador rejeitará os códigos 4 e 5.

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
