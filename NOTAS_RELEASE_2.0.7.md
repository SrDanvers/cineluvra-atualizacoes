# Cineluvra 2.0.7 — atualização obrigatória

Nova versão preparada no Android Studio, preservando a interface lilás original, a área do criador, o ícone, o catálogo, os filmes, as séries, os animes e Chiquititas.

A partir da versão 2.0.7, o aplicativo consulta `update.json` ao iniciar. Se houver versão posterior com `forceUpdate: true`, apresenta aviso obrigatório com botão **Atualizar agora** e não libera o catálogo até a atualização. Sem atualização pendente, abre normalmente. A exigência já conhecida permanece registrada localmente se a internet falhar.

A versão 2.0.6 já instalada não possui esse bloqueio nativo. Para ativá-lo, a versão 2.0.7 precisa ser compilada, testada e distribuída com assinatura Android compatível.

**O `update.json` só deve ser alterado depois de publicar um APK válido na Release e comparar a assinatura com as versões anteriores.** O Android exige consentimento do usuário para instalar um APK.

Criado por Denny Ximenes.
