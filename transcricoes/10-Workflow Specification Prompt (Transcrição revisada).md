Bom, pessoal, eu acho que com esses últimos vídeos, que inclusive acabam sendo um pouco repetidos, mas novamente, galera, a gente está falando de prompt. Eu quero gerar a maior quantidade de insights possíveis para vocês. Então, o que acontece é o seguinte: esses tipos de prompt eu acredito que já ficou claro aí na sua mente. Agora, eu quero falar desse camarada aqui, que são prompts específicos que a gente utiliza para workflows.

Então, vamos lá. Eu vou fechar esse cara aqui e vou abrir para esse camarada que ele é um comando. Esse comando, no final das contas, é um comando que o Cloud Code executa. Então, entenda uma coisa: apesar disso aqui ser um comando que é executado via Cloud Code, é importante você saber que um comando ou um prompt pode ser executado em qualquer inteligência artificial. Mas especificamente esse comando, eu faço com que ele trabalhe de forma multi-agentes. E por isso que é importante você entender a estrutura desse cara.

E somente para você saber, não necessariamente você precisa trabalhar de forma multi-agentes para ter um prompt que vai forçar um workflow de uma forma mais detalhada. Nesse caso aqui, eu acho que fica bacana porque dá para você ter um pouco mais de clareza de como tudo isso aqui ficou.

Então, aqui é o nome do meu comando. Basicamente aqui é uma forma de eu ler e entender do que aquilo se trata. É muito mais sobre isso do que necessariamente mandar ele fazer. Apesar do que o nome acaba já ajudando a entender aquele contexto, mas aqui basicamente eu estou trazendo uma descrição que é o seguinte: produza de forma completa e auditável um snapshot de um projeto coordenando agentes especialistas e consolidando as outputs deles.

E aqui, galera, é uma forma de eu estar tentando definir semanticamente o que cada agente pode ser e como ele é nomeado. Por quê? Porque o próprio Cloud Code, nesse caso, ele é um agente. Então, toda vez que eu falei Cloud Code entre parênteses e U, ele sabe que eu estou falando com o agente principal dele. E eu estou falando que ele funciona como um coordenador. O orquestrador, o agente orquestrador, somente vai preparar uma estrutura para depois sintetizar os outputs.

E aqui, galera, novamente, é o ponto mais importante de todos, que é o output. Se você olhar aqui nessa minha descrição, de uma forma geral, eu estou dando um output na descrição aqui desse cara. Mas como o foco desse nosso amigo aqui é gerar muito mais, focar muito mais no workflow, eu não estou, na realidade, pegando tão pesado em como que vai ser todos os detalhes do output, apesar de eu colocar um template abaixo.

Mas o ponto principal aqui é que eu estou falando aqui: sua final delivery, ou seja, o que você vai entregar como resultado final, basicamente é tudo que esse cara faz. Apesar de ele gerar vários efeitos colaterais, fazendo com que múltiplos agentes sejam chamados, no final do dia ele vai gerar um readme nesse formato aqui usando a data atual para não ter perigo, que vai ser gravado dentro do diretório do agente orquestrador — isso aqui foi opção minha —, com uma descrição do projeto e com um índice linkando todos os relatórios produzidos pelos agentes.

Então, quando você criar o readme, vai ser um índice listando os arquivos por arquivos, usando o caminho absoluto, começando pela barra do repositório que ele está trabalhando. Então, aqui eu dei um exemplo de como é um markdown. Então, project architecture barra o link to report. É assim que em markdown a gente define um link.

Então, eu também pedi para ele na descrição, para ele validar todo o link antes de salvar no readme, para garantir que o caminho existe. Use o manifest.md, gerenciado pelo orquestrador, o agente orquestrador — a gente vai falar dele mais tarde —, como fonte da verdade para mapear todos os reports. Isso vai ser inicializado na fase 1 e vai ser alterado a cada vez que um agente completa as fases. Daí a gente vai falar um pouco mais sobre essas fases ali.

E aqui eu dei um output template, se você olhar aqui para a gente. Output template. O que o output template? Como que eu quero de resultado final? Então aqui eu falo o que a parte que vai ser entregue, que vai ser um... Aqui eu estou definindo como que vai ser esse índice. Eu fiz de uma forma bem simples: nome do projeto, uma descrição breve do projeto, uma descrição explicando sobre os pontos principais desse documento com a consolidação e os aspectos principais do projeto, como se fosse um raio-x.

Pedi para ele colocar a data de geração. Coloquei um overview e a arquitetura do software. Então tem um project overview, caso queira um project architecture, os componentes e as dependências. Perceba que cada cara desse é um agente diferente que vai chamar. E aqui eu coloquei também critical constraints, ou seja, restrições críticas.

Nunca dê o fluxo completo para o agente orquestrador. O orquestrador somente executa algo com duas responsabilidades: na fase 1, para criar o projeto, a estrutura do projeto, ou de forma explícita, quando a gente fala o folder, o output folder, ou os folders que vão ser ignorados. Fase 4, que ele vai sintetizar todos os relatórios gerados pelos agentes.

Pedir para ele ser de forma estrita, extremamente restritivo pela separação dos agentes. Ou seja, invoque cada agente especialista e separe para cada tarefa. O orquestrador, o agente orquestrador não deve chamar subagentes. O Cloud Code vai ser responsável por coordenar a sequência. Então, o orquestrador — e a gente vai falar de orquestrador daqui para frente também — ele não vai ser o cara responsável por chamar os agentes. Quem faz isso é o Cloud Code. O orquestrador apenas mantém o tracking do que já foi feito.

E aqui eu falei: siga exatamente o que está escrito na especificação de cada agente. Então, isso eu estou garantindo para fazer com que ele leia o conteúdo de cada agente para evitar com que ele esqueça qualquer coisa.

Nunca escreva os outputs fora das pastas que foram pedidas. Nunca dê recomendações ou planos de ação. Novamente porque eu não quero isso. Eu quero um raio-x só do projeto. Nunca traga o tempo de duração. Evite linguagens vagas como "isso aqui é probably safe" ou "isso pode dar certo, pode ser bom". Não fabrique CVEs — basicamente os bancos de dados de vulnerabilidades —, ou seja, somente traga essas vulnerabilidades se você conseguir ver que foram produzidas pelo nosso agente de auditoria.

E aqui, eu coloquei ainda essas constraints bem específicas. Pontos importantes para a separação de agentes: cada agente tem que ser invocado numa task separada. Ou seja, eu vou fazer uma chamada, uma tool call, que vai ser uma tarefa. O agente orquestrador não deve ser pedido para gerar subagentes para ele mesmo. Você é o Cloud Code, você é o coordenador, não é o orquestrador.

Estou tentando deixar bem claro que coordenador é o cara que vai gerar os agentes, que está recebendo o comando, e o orquestrador é o cara que mantém o progresso dos relatórios que vão ser feitos para serem sintetizados e gerar o relatório final.

Todas as comunicações acontecem por você. Você decide quando um novo agente começar. Depois que um agente finalizar, você precisa chamar o orquestrador para alterar o manifesto. Na prática, isso é o mínimo. Toda vez que a gente vai chamar uma task orchestrator, uma vez que essa tarefa é completada, você tem que fazer alteração no manifesto. Basicamente é isso.

Então, eu dei um exemplo: quando uma tarefa para o architecture analyzer for completada, você tem que invocar o orquestrador para guardar no manifesto.md que essa tarefa foi terminada. Nem sempre o Cloud vai querer trabalhar dessa forma. Às vezes eu peço e ele faz isso, às vezes ele espera eu terminar os relatórios para sintetizar tudo, tá galera? Novamente, depois se você estiver se incomodando muito com o comportamento que ele não está trabalhando para você, o que você pode fazer? Você pode ser ainda mais específico ali em alguns pontos.

Aqui, galera, é o ponto de ouro, que é o workflow que vai ser executado. E uma das formas bem simples — que garante de uma forma... garante não — que maximiza a chance de sucesso para que esse workflow seja seguido é você separar por fases o fluxo daquilo que vai ser executado.

Então, o que acontece? Eu coloquei fase 1 e eu coloquei uma tarefa entre parênteses, o nome do agente, para ficar mais claro para ele entender. Então, entenda as flags para trabalhar e entender os caminhos, porque eu posso ter diversos caminhos dentro dos meus diretórios, porque esse orquestrador ele vai ter que entender realmente a estrutura de projetos do meu arquivo, porque ele vai ter que gerar um manifesto. Respeite o `--project-folder`, `--output-folder` quando provided. Se não for provided, use as localizações padrão que vão ser dadas pelo orquestrador, por exemplo.

Crie somente os diretórios requeridos pela especificação do orquestrador. Não crie sub-levels de diretórios ou reports, a não ser que tenha uma especificação. Ignore a lista... Qualquer tipo de lista antes de ler. Ou seja, nunca faça o particionamento. Escaneie os arquivos que estão em qualquer pastas, dentro desse parâmetro ignore folders. Por quê? Lá embaixo eu vou mostrar para você como é que vai ser o comportamento.

E inicialize o manifesto.md do orquestrador dentro do diretório em branco com a seguinte estrutura: título, o caminho absoluto, o agente e o timestamp. Porque esse cara aqui que vai medir o que já foi feito.

E agora aqui eu tenho a fase 2. Por exemplo, inicialize na fase 2 uma tarefa para o auditor de dependências e o architectural analyzer. E eu estou falando aqui em parallel. Ou seja, eu estou falando para o Cloud Code aqui nesse caso: olha, na hora que você chegar nessa fase 2, suba dois agentes de uma vez. Eu não preciso rodar primeiro o auditor e depois o de arquitetura. Então, o lance aqui é importante.

E aqui eu separo essa tarefa em duas partes. Parte 1, auditor. Ele faz um relatório completo de dependências no sistema, baseado na especificação do agente, importante para a dependency validation nessa tarefa. Use o MCP servers como o Context 7 e o FireCrawl para verificar as versões, o nível de manutenção, o status de manutenção, as vulnerabilidades ali daquele pacote.

Então, perceba que essas instruções aqui vão ser passadas para esse agente auditor. Então, por isso que eu estou colocando o que tem que ser passado de informação.

E aqui, o cara de análise de arquitetura, que vai produzir um relatório completo de arquitetura seguindo as especificações do agente. Somente o orquestrador vai guardar informação no manifesto.md quando cada task completar. O que isso significa no final das contas? Que o Cloud Code não vai sair modificando o manifesto.md.

Aqui é a parte mais interessante, na minha opinião, que é a fase 3. Uma vez que eu tenho esses dois relatórios gerados, essa fase 3 depende principalmente desse relatório aqui, do relatório de arquitetura, porque nesse relatório de arquitetura a gente tem os componentes.

Então, aqui na fase 3, ele vai fazer um agente em paralelo para analisar o componente de uma forma específica. Um por componente. Então, faça parte do report de arquitetura, que foi feito na fase 2, tratando isso como um artefato pelo Architecture Analyzer. Também, para cada componente listado, por exemplo, na seção Critical Component Analysis, na seção ou em outras seções que mostrem componentes, inicie um agente separado, Task Deep Analyzer, para cada componente em paralelo.

Para cada tarefa, você tem que analisar somente o componente que foi passado para esse cara. Você tem que cobrir... Aqui eu estou dando um exemplo para ele. Por que eu estou dando um exemplo? Porque às vezes ele não entendia que era para ele gerar um relatório por componente. Então, fui mais específico.

Ou seja, como ele vai fazer a cobertura? Se o relatório de arquitetura tem 10 componentes, você precisa rodar 10 agentes em paralelo na execução, gerando, então, 10 relatórios. Nenhum componente pode ser escapado, pode ser pulado.

Depois que essa tarefa foi feita, as execuções completas, você precisa verificar se todos os reports foram feitos. Então, reabra o arquivo e reveja essas seções linha por linha. E se algum componente não foi feito o report, faça, gere mais um Deep Analyzer para executar até que a cobertura seja de 100%. Vamos imaginar que o Cloud delirou em algum momento e ele esqueceu um componente. Então aqui é uma forma de eu reverificar se realmente todos os componentes foram feitos. Então é uma parte de análise.

E aqui eu coloquei o importante: tenha certeza que você não vai duplicar o report. E aqui eu usei uma palavra-chave, principalmente para o Cloud, que é UltraThink. UltraThink vai fazer com que ele pense de uma forma ainda mais estruturada, para ele conseguir perceber que não existe, para ele não duplicar relatório.

Por quê? Às vezes ele vê um relatório com uma data e hora, e ele pode ler e ver que esse relatório não existe, e ele acaba podendo até duplicar relatório. Isso aconteceu comigo. Então, eu pedi para ele verificar com UltraThink mesmo, para ver se existe algum relatório já criado com nomes similares com timestamp etc. Eu falei: você tem que ser extremamente preciso nessa verificação.

A fase 4 para fazer com que o orquestrador nosso pegue todos os relatórios gerados e finalize o manifesto.md para ter todos os relatórios gerados.

E aqui, a fase 5 é pedir para ele, o Cloud Code, ler o manifesto, validar que todos os arquivos existem, salvar um arquivo readme com esses detalhes dentro do diretório do orquestrador. Lembrando que o orquestrador agente é somente mais um especialista, que faz o setup na fase 1, a síntese na fase 4, e ele não coordena os agentes, porque esse é o job dele, o Cloud Code.

E aqui, galera, eu coloquei exemplos de utilização. Então, aqui, execution... cadê aqui? Exemplos de utilização. Então, aqui é o seguinte, galera: como eu vou chamar esse comando no Cloud Code, eu posso passar parâmetros para deixar mais claro para o agente o que eu quero fazer. Então eu estou colocando: use os argumentos que vão ser passados ali para a gente conseguir setar pastas de entrada, pastas de saída e etc.

Então eu falei o seguinte: nunca use nenhum outro caminho para salvar relatórios, arquivos ou manifestos a não ser que eu passe especificamente pelo usuário, para ele não criar também subfolders chamado reports, outputs ou qualquer coisa desse tipo. Nunca crie nenhum outro arquivo que não seja especificado pelo agente. Siga o seguinte padrão de output.

Então, o que acontece é o seguinte. Eu estou definindo aqui como que eu vou rodar esse comando. Então, eu posso rodar esse comando para ele fazer essa chamada direta no Cloud Code, ou eu posso fazer o seguinte: rodar o workflow no projeto somente na pasta que eu quero. Então, eu posso passar `--project-folder` e passar a pasta. Isso vai fazer com que ele faça análise somente dentro daquela pasta. Às vezes eu tenho um monorepo, eu quero analisar um projeto só daquele monorepo e não todos.

Outra coisa que eu pedi para ele fazer também é fazer o seguinte: eu poder especificar qual é a pasta de saída que eu vou querer, porque por padrão está `/docs/agente/` e o nome do relatório. Aqui eu estou falando para ele seguir o output na pasta que eu passei.

E não menos importante, eu também pedi para ter um parâmetro onde eu passo para ele ignorar alguns arquivos. Então, imagina que tem pastas que você acha que não vale a pena ele analisar, que tem outra coisa que não tem nenhum sentido, então você consegue dar um `--ignore-folders` para ele ignorar e não analisar essas pastas.

Instruções negativas, de uma forma bem forte: nunca modifique o codebase, não faça upgrades, não invente CVEs, não use linguagem vaga, não use emojis, não provide timestamp. Perceba que essas instruções negativas, elas são muito parecidas com as que a gente já foi. Aqui eu só fui, trouxe, organizei mais os bullets para ficar mais claro aqui para ele e trouxe também observações.

E novamente eu pedi aqui para ele: UltraThink, pense passo a passo. Aqui eu já estou usando a chain of thoughts, para determinar de forma mais clara a instrução para que cada agente possa completar a tarefa.

Por que eu estou dizendo isso? Porque o Cloud Code, ele vai ser responsável para chamar um agente. Para ele chamar esse agente, ele tem que mandar uma mensagem. Para essa mensagem ser mandada, essa mensagem tem que ser muito bem pensada para ele não passar simplesmente de uma forma bem vaga e esse cara não vai fazer um bom trabalho.

Então, eu estou pensando aqui para ele, falando o seguinte: você como coordenador, master, você tem que prover toda a informação necessária de contexto para cada agente para garantir que todo agente consiga entender passo a passo o que ele precisa fazer. O agente orquestrador ele vai sempre fazer um append no manifesto imediatamente, toda vez que o agente terminar. E basicamente é isso, mas eu acho que dar observação aqui, galera, esse é o passo mais importante, porque aqui eu estou pedindo para ele realmente refletir tudo o que ele precisa passar para o agente que ele vai chamar para garantir que não vai passar instruções faltantes, fazendo com que esse agente não consiga concluir o trabalho dele.

Isso aqui que eu estou passando para vocês, pessoal, nesse prompt não é somente para esse tipo de contexto. Isso aqui é muito utilizado em Prompt Engineering quando você está trabalhando em aplicações multi-agênticas. E normalmente, inclusive, a gente seta um formato de chamada de um agente para o outro. Muitas vezes a gente chama de... a gente faz uma chamada em JSON falando: você vai passar isso, isso, o next step é isso, a observação é isso, para garantir um protocolo claro de comunicação. Nesse caso a gente não está fazendo isso, tá?

Então, sei que ficou grande esse vídeo, mas era importante você entender essa parte aqui. E aí.
