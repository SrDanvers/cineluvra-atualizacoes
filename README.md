# Cineluvra — atualizações Android

Canal público de atualizações do aplicativo Cineluvra, criado por Denny Ximenes.

- O arquivo `update.json` é gerado pelo workflow após a publicação de uma Release válida.
- Cada Release precisa conter **um** APK assinado com o certificado original e tag `vX.Y.Z`.
- O aplicativo consulta o manifesto para informar quando existe uma atualização.
- A instalação depende da confirmação do usuário no Android.

**Segurança:** não enviar projeto Android privado, chaves `.p12`/`.jks`, senhas, tokens ou backups para este repositório.

Versão inicial planejada: `v1.1.1` (Android `versionCode` 4, pacote `br.com.dennyximenes.cineluvra`).
