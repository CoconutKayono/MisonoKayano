from pathlib import Path
import base64, html

HERE = Path(__file__).resolve().parent
TARGET = Path(r'D:/Work Env/MisonoKayano/Notes/Nertwork/通过幂等API实现安全重试-中文全文.html')

def img(name, alt, cls=''):
    data = base64.b64encode((HERE / name).read_bytes()).decode('ascii')
    return f'<img class="{cls}" src="data:image/png;base64,{data}" alt="{html.escape(alt)}">'

def code(text):
    return '<pre><code>' + html.escape(text.strip('\n')) + '</code></pre>'

def figure(name, title, labels):
    rows = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a,b in labels)
    return '<figure>' + img(name,title) + f'<figcaption>{title}（保留原图）</figcaption></figure><div class="table-scroll"><table><caption>图中文字的完整中文对照（重复出现的标签译法相同）</caption><thead><tr><th>原文</th><th>中文</th></tr></thead><tbody>{rows}</tbody></table></div>'

pages = []
pages.append('''<div class="cover"><div class="eyebrow">AWS · 中文全文译本</div><h1>通过幂等 API 实现安全重试</h1><div class="english-title">Making retries safe with idempotent APIs</div><p class="author">Malcolm Featonby</p>''' + img('page-1-image-1-Im0.png','AWS 标志','aws-logo') + '''<div class="cover-footer"><strong>通过幂等 API 实现安全重试</strong><p>版权所有 © 2020 Amazon Web Services, Inc. 和／或其关联公司。保留所有权利。</p></div></div>''')

pages.append('''
<p>在 Amazon，我们经常在服务中看到这样一种模式：将一个复杂操作拆解，由一个控制流程调用多个较小的服务，每个服务负责整体工作流中的一个部分。例如，启动一个 Amazon Elastic Compute Cloud（EC2）实例。在其内部实现中，这涉及调用负责决定实例部署位置、创建 Amazon Elastic Block Store（EBS）卷、创建弹性网络接口，以及预置虚拟机（VM）的服务。有时，其中一个或多个服务调用可能失败。为了提供良好的客户体验，我们希望推动这个工作流最终成功。为此，我们依靠控制流程，引导所有拆分出的服务进入已知的正常状态。</p>
<p>我们发现，在许多情况下，最简单的解决方案就是最好的解决方案。在刚才描述的场景中，最好的办法是直接重试这些调用，直到成功。有意思的是，正如 Marc Brooker 在<a href="https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/">《超时、重试与带抖动的退避》（Timeouts, retries, and backoff with jitter）</a>一文中所解释的，仅仅通过重试调用，就能克服数量多得令人惊讶的瞬时故障或随机故障。这种模式看似简单，却已被证明非常有效，因此我们在一些 AWS SDK 实现中内置了<a href="https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/retry/PredefinedRetryPolicies.SDKDefaultRetryCondition.html">默认重试行为</a>。这些实现会自动重试因网络 I/O 问题、服务端故障或服务限流而失败的请求。能够直接重试请求，减少了客户端需要处理的边界情况。因此，调用服务所需的、无法形成差异化价值的样板代码也随之减少。在这里，这类样板代码指的是：为了处理可能发生的各种故障场景，在对远程服务的调用外面增加的包装代码。</p>
<p>不过，把重试服务调用作为缓解瞬时故障的措施，是建立在一个简化假设上的：可以重试某个操作，而不会产生任何副作用。换句话说，即使我们需要在重试循环中多次发起调用，也要确保该调用的结果只发生一次。回到前面的例子：如果 EC2 实例启动工作流重试了一次失败的 EBS 卷创建调用，最终却得到两个 EBS 卷，这显然不是我们希望看到的结果。在本文中，我们将讨论 AWS 如何利用幂等 API 操作，减少重试可能带来的一些不期望出现的副作用，从而提供更健壮的服务，同时仍然利用重试的优势来简化客户端代码。</p>
<h2 id="side-effects">重试及其可能带来的不期望出现的副作用</h2>
<p>为了更深入地探讨这一点，我们来看一个假想场景：一位客户正在使用 Amazon EC2 的 <code>RunInstances</code> API 操作。在这个场景中，客户希望运行一个单例工作负载，也就是要求任意时刻“至多一个”（at most one）EC2 实例处于运行状态的工作负载。为此，客户的预置流程请求 Amazon EC2 启动这个新工作负载。然而，由于某种原因——可能是网络超时——预置流程没有收到响应。</p>
''')

pages.append(figure('page-3-image-1-Im0.png','图 1：单例工作负载的启动请求没有收到响应',[
('Customer work orchestrator','客户工作编排器'),('EC2 RunInstances','EC2 RunInstances'),('Singleton Workload','单例工作负载'),('No response received','未收到响应')]) + '''
<p>这让预置流程陷入了两难：无法确定单例工作负载是否已经在运行。直接重试请求可能导致多个工作负载同时存在，而这可能造成严重后果。为了摆脱这一困境，预置流程必须执行一次核查与对账（reconciliation），判断该工作负载是否正在运行。为了补偿一个可能相对罕见的边界情况，需要做这么多工作，负担很重。而且，即使执行了核查工作流，仍然可能存在不确定性。如果资源确实存在，但它是由另一个预置流程创建的，怎么办？在简单情况下，这也许没有问题；但在更复杂的场景中，弄清资源究竟是由当前流程还是另一个流程创建的，可能十分重要。</p>
<h2 id="design">通过幂等 API 设计降低客户端复杂度</h2>
<p>为了让调用方可以重试这类操作，我们需要使它们具有幂等性。幂等操作是指：请求可以被重新传输或重试，而不会产生额外的副作用。这种性质对分布式系统非常有益。</p>
<p>如果我们提供的契约允许客户端做出一个简化假设——只要错误不是校验错误，就可以通过重试请求直到成功来克服——就能够显著简化客户端代码。不过，这也会给服务实现增加一些复杂度。在一个分布式系统中，许多客户端发起大量调用，同时有大量请求正在处理中；这时，挑战在于：如何识别某个请求是之前某个请求的重复？</p>
<p>可以采用许多方法来推断某个请求是否是先前请求的重复。例如，也许可以根据请求参数生成一个合成令牌。可以对请求中的参数计算哈希，并假定同一调用方发出的、参数完全相同的请求都是重复请求。表面上看，这似乎能同时简化客户体验和服务实现：凡是看起来与先前请求完全相同的请求，都被视为重复请求。然而，我们发现这种方法并不适用于所有情况。例如，同一调用方在很短的时间内发送两个完全相同的 Amazon DynamoDB 表创建请求，把它们看作同一个请求的重复可能是合理的。但是，如果这些请求是为了启动 Amazon EC2 实例，这个假设可能就不成立。调用方可能确实想要两个完全相同的 EC2 实例。</p>
''')

pages.append('''
<p>在 Amazon，我们更倾向于在 API 契约中加入由调用方提供的唯一客户端请求标识符。同一调用方发出的、客户端请求标识符相同的请求，可以被视为重复请求，并据此处理。通过让客户借助 API 语义清楚地表达意图，我们希望降低客户遇到意外结果的可能性。对幂等操作而言，由调用方提供的唯一客户端请求标识符满足了这一需求。它还有一个好处：这种意图很容易被审计，因为这个唯一标识符会出现在 AWS CloudTrail 等日志中。此外，通过用唯一客户端请求标识符标记创建出的资源，客户能够识别任意给定请求所创建的资源。Amazon EC2 的 <code>DescribeInstances</code> 响应就是一个具体例子：它会显示创建该 EC2 实例时使用的唯一标识符。（在 Amazon EC2 API 中，这个唯一客户端请求标识符称为 <code>ClientToken</code>。）</p>
<p>下图展示了一个示例请求／响应流程，在幂等重试场景中使用了唯一客户端请求标识符：</p>
''' + figure('page-4-image-1-Im0.png','图 2：使用唯一客户端请求标识符进行幂等重试',[
('Client','客户端'),('Service','服务'),('StateStore','状态存储'),('Time','时间（向下推进）'),
('CreateResource(Name = X, ClientRequestIdentifier = 123)','创建资源（Name = X，ClientRequestIdentifier = 123）'),
('Get and Set ClientRequestIdentifier','读取并设置客户端请求标识符（ClientRequestIdentifier）'),
('Service request','处理请求'),('Update ClientRequestIdentifier response state','更新客户端请求标识符对应的响应状态'),
('Response fails to reach client','响应未能到达客户端'),
('Retry CreateResource(Name=X, ClientRequestIdentifier = 123)','重试创建资源（Name = X，ClientRequestIdentifier = 123）'),
('Service identifies that request has already been serviced. Prepares a semantically equivalent response.','服务识别出该请求已被处理，准备一个语义等价的响应。'),
('Response delivered to client','响应送达客户端')]) + '''
<p>在这个例子中，客户请求创建一个资源，并在请求中提供唯一客户端请求标识符。服务收到请求后，首先检查以前是否见过这个标识符。如果没有，就开始处理请求。它会为这个请求创建一个幂等“会话”，以客户标识符和客户提供的唯一客户端请求标识符作为键。如果随后收到来自同一客户、使用同一唯一客户端请求标识符的请求，服务就知道自己已经见过这个请求，并可以采取适当的措施。一个重要的考虑是：记录幂等令牌，以及为处理请求而执行的全部修改操作，两者结合起来的过程必须满足原子性、一致性、隔离性和持久性（<a href="https://sites.fas.harvard.edu/%7Ecs265/papers/haerder-1983.pdf">ACID</a>）操作的性质。服务端的 ACID 操作必须是“要么全部完成，要么全部不做”的原子过程。这能确保我们避免以下情况：记录了幂等令牌，却未能创建某些资源；或者反过来，创建了资源，却未能记录幂等令牌。</p>
''')

pages.append('''
<p>上一张图展示了在请求已经被见过的情况下，准备一个语义等价响应的过程。有人可能会认为，要严格满足幂等操作的字面要求，并不需要这样做。设想一个假想的 <code>CreateResource</code> 操作，调用时使用唯一请求标识符 <code>123</code>。如果第一个请求已被收到并处理，但响应始终没有返回调用方，那么调用方会使用标识符 <code>123</code> 重试请求。然而，资源此时可能已经在最初的请求中创建好了。一种可能的处理方式是返回 <code>ResourceAlreadyExists</code> 返回码。这满足幂等性的基本原则，因为重试调用没有产生副作用。不过，从调用方的角度看，这会带来不确定性：不清楚资源究竟是由当前这个请求创建的，还是由更早的请求创建的。这也会让把重试引入为默认行为变得更有挑战性。原因是，尽管请求没有产生副作用，但后续重试及其返回码很可能改变调用方的执行流程。现在，即使在调用方看来，发起调用之前资源还不存在，它也必须处理资源已经存在的情况。在这个场景中，虽然从服务的角度没有副作用，但返回 <code>ResourceAlreadyExists</code> 却从客户端的角度产生了副作用。</p>
<h2 id="semantics">语义等价与对默认重试策略的支持</h2>
<p>另一种做法是：在某个时间区间内，对于同一唯一请求标识符，始终提供语义等价的响应。这意味着，同一调用方使用同一唯一客户端请求标识符发起重试请求时，后续返回的任何响应，都与第一个成功请求所返回的第一次响应具有相同的含义。这种方法具有一些非常有用的性质，尤其适用于我们希望通过安全、简单地重试遭遇服务端故障的操作来改善客户体验的情况，就像我们通过 AWS SDK 的默认重试策略所做的那样。</p>
<p>使用 Amazon EC2 的 <code>RunInstances</code> API 操作和 AWS Command Line Interface（CLI，命令行界面），我们可以看到一个实际例子：幂等性、语义等价响应和自动重试逻辑如何共同工作。请注意，AWS CLI 与 AWS SDK 一样，<a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-retries.html">支持默认重试策略</a>，这里使用的就是该策略。在这个例子中，我们通过下面的 AWS CLI 命令启动一个 EC2 实例：</p>
''' + code('''$ aws ec2 run-instances --image-id ami-04fcd96153cb57194 --instance-type t2.micro
{
    "Instances": [
        {
            "Monitoring": {
                "State": "disabled"
            },
            "StateReason": {
                "Message": "pending",
                "Code": "pending"
            },
            "State": {''') + '<div class="continuation">代码续见下一原页。</div>')

pages.append('<div class="continuation">接上一原页的代码。</div>' + code('''                "Code": 0,
                "Name": "pending"
            },
            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "ImageId": "ami-04fcd96153cb57194",
            …
            "ClientToken": "eb3c3141-a229-4ca0-b005-eb922e2cabdc",
            …''') + '''
<p>在许多 AWS API 操作中，唯一客户端请求标识符通过 <code>ClientToken</code> 字段建模。请注意，我们没有在请求中提供唯一客户端请求标识符。响应中的 <code>ClientToken</code> 属性是由远程服务回传的。这是因为，如果请求没有提供标识符，AWS CLI 就会为它生成一个唯一 ID；这样，在上游服务发生瞬时故障时，重试就可以在内部自动进行。要模拟一次重试请求／响应可能是什么样子，可以等待几分钟，然后使用 AWS CLI 再发起一个请求，使用上一个请求返回的同一个 <code>ClientToken</code>。需要注意的是，返回的响应与第一次响应非常相似，但并不完全相同：</p>
''' + code('''$ aws ec2 run-instances --image-id ami-04fcd96153cb57194 --instance-type t2.micro --client-token eb3c3141-a229-4ca0-b005-eb922e2cabdc
{
    "Instances": [
        {
            "Monitoring": {
                "State": "disabled"
            },
            "StateReason": {
                "Message": "running", ← 现在正在运行
                "Code": "running"  ← 现在正在运行
            },
            "State": {
                "Code": 16,  ← 现在为运行状态码
                "Name": "running"  ← 现在正在运行
            },
            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "ImageId": "ami-04fcd96153cb57194",
            …
            "ClientToken": "eb3c3141-a229-4ca0-b005-eb922e2cabdc",
            …''') + '''
<p>只要这种行为可用，AWS SDK 和 AWS CLI 就会利用它来简化客户使用这些工具时的体验。我们的 SDK 和 CLI 知道哪些操作支持幂等契约；如果调用方没有提供唯一客户端请求标识符，它们就会生成一个，并将其加入请求。如果发生重试，就复用这个已经生成的标识符，从而确保满足对该请求“至多一次”（at most once）的承诺。因为响应——即使是重试的响应——也具有语义等价性，所以调用方的客户端代码可以完全不知道 SDK 代码内部发生了任何重试，只需在收到响应时处理它即可。</p>
''')

pages.append('''
<h2 id="late">迟到的请求与唯一客户端请求标识符的生命周期</h2>
<p>在分布式系统的幂等解决方案中，请求迟到可能引发一种有意思的边界情况。设想这样一种情况：有两个参与者与一个服务交互。创建资源的客户端重试了操作，而后续请求被延迟了。在此期间，第二个参与者删除了该资源：</p>
''' + figure('page-7-image-1-Im0.png','图 3：资源已被删除后，迟到的重试请求才到达',[
('ClientA','客户端 A'),('ClientB','客户端 B'),('Service','服务'),('StateStore','状态存储'),('Time','时间（向下推进）'),
('CreateResource(Name = X, ClientRequestIdentifier = 123)','创建资源（Name = X，ClientRequestIdentifier = 123）'),
('Get and Set ClientRequestIdentifier','读取并设置客户端请求标识符（ClientRequestIdentifier）'),('Service request','处理请求'),
('Update ClientRequestIdentifier response state','更新客户端请求标识符对应的响应状态'),('Response fails to reach client','响应未能到达客户端'),
('DeleteResource(Name=X)','删除资源（Name = X）'),('Resource deleted','资源已删除'),
('Retry CreateResource(Name=X, ClientRequestIdentifier = 123)','重试创建资源（Name = X，ClientRequestIdentifier = 123）'),
('Determine already serviced request. Prepare a semantically equivalent response based on ClientRequestIdentifier response state','判定请求已经被处理。根据客户端请求标识符对应的响应状态，准备一个语义等价的响应。'),
('Response to client','向客户端返回响应')]) + '''
<p>应对这个场景的最佳方式，可能因服务而异。对于 EC2 的 <code>RunInstances</code>，我们采用的做法是：即使在刚才描述的场景中，也遵守最初的幂等契约。在这种情况下，我们遵循最小惊讶原则（principle of least astonishment）。这意味着，即使资源已经被删除，也返回语义等价的响应；这是最不令人意外的做法，同时仍然能够在使用 AWS SDK 和 AWS CLI 等工具时提供一致的体验。</p>
<p>沿用前面的 EC2 实例启动示例，我们可以终止之前启动的 EC2 实例，来模拟这一边界情况：</p>
''' + code('''$ aws ec2 terminate-instances --instance-ids i-xxxxxxxxxxxxxxxxx
{
    "TerminatingInstances": [
        {''') + '<div class="continuation">代码续见下一原页。</div>')

pages.append('<div class="continuation">接上一原页的代码。</div>' + code('''            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "CurrentState": {
                "Code": 32,
                "Name": "shutting-down"
            },
            "PreviousState": {
                "Code": 16,
                "Name": "running"
            }
        }
    ]
}''') + '''
<p>如果接下来使用相同的参数和唯一请求标识符，对 <code>RunInstances</code> API 请求进行一次模拟的“迟到”重试，就会得到语义等价的响应。不过，如下面的示例所示，实例此时已经终止：</p>
''' + code('''$ aws ec2 run-instances --image-id ami-04fcd96153cb57194 --instance-type t2.micro --client-token eb3c3141-a229-4ca0-b005-eb922e2cabdc
{
    "Instances": [
        {
            "Monitoring": {
                "State": "disabled"
            },
            "StateReason": {
                "Message": "terminated", ← 现在已终止
                "Code": "terminated"  ← 现在已终止
            },
            "State": {
                "Code": 48, ← 已终止状态码
                "Name": "terminated"  ← 现在已终止
            },
            "InstanceId": "i-xxxxxxxxxxxxxxxxx",
            "ImageId": "ami-04fcd96153cb57194",
            …
            "ClientToken": "eb3c3141-a229-4ca0-b005-eb922e2cabdc",
            …''') + '''
<p>为了支持这种行为，我们需要在服务中保留最初那次幂等请求的信息。不过，无限期保留这些信息并不现实。如果未来的某个请求标识符与很久之前使用过的标识符发生冲突，无限期保留还可能对客户体验产生不良影响。不同服务及其资源，对保留时间的要求有所不同。我们发现，对于 EC2 实例，将这个时间范围限制为资源的存活期，再加上一段额外时间，是可行的。在这段额外时间过后，可以合理地假定：任何迟到的请求，要么已经到达，要么已经不再有效。</p>
''')

pages.append('''
<h2 id="parameters">后续调用保持相同的客户端请求 ID，却改变了请求参数时，如何响应</h2>
<p>我们设计 API 的目的，是让客户能够明确表达自己的意图。设想这样一种情况：我们收到一个之前见过的唯一客户端请求令牌，但请求中的参数组合与此前的请求不同。我们发现，最稳妥的做法是认为客户想要一个不同的结果，因此这可能不是同一个请求。对于这种情况，我们返回一个校验错误，指出幂等请求之间存在参数不匹配。为了支持这种深入校验，我们还会把最初请求使用的参数与客户端请求标识符一起存储。</p>
<h2 id="conclusion">结论</h2>
<p>Amazon 首席技术官 <a href="https://www.allthingsdistributed.com/2016/03/10-lessons-from-10-years-of-aws.html">Werner Vogels</a> 指出，我们在 Amazon 学到的一条经验，是要预期意外情况的发生。他提醒我们，故障不可避免，因此最好构建能够把故障当作自然现象来接纳的系统。围绕这些故障编写应对代码，是一项重要但无法形成差异化价值的工作；它能提高交付方案的完整性与可靠性，却也占用了原本可以投入到差异化代码中的时间。</p>
<p>在前文提到的《超时、重试与带抖动的退避》（Timeouts, retries, and backoff with jitter）一文中，Marc Brooker 展示了我们如何利用重试缓解瞬时故障，以及如何在 SDK 和工具中自动执行这些重试来改善易用性。在那篇文章的基础上，本文探讨了 AWS 如何利用幂等行为，让客户获得自动重试策略的益处，同时仍然遵守某些操作的 API 契约中内含的“至多一次”承诺。</p>
<p>我们发现，本文介绍的方法效果良好，也听到客户表示，他们很认可这种方法带来的复杂度降低。不过，要构建满足本文所述契约的服务，本身就需要付出成本并承担复杂度，而这种复杂度并不适合所有解决方案。有时，最好投入额外时间，满足本文所述的更严格契约的要求；在另一些情况下，最好采用较简单的契约来更快地创新，因为这才最符合客户的利益。对于需要更严格“至多一次”契约的场景，我们发现，本文的方法能够很好地满足客户需求。</p>
''')

css = '''
:root{--ink:#203043;--muted:#607086;--orange:#ff9900;--border:#dce3eb;--paper:#fff;--bg:#f0f3f7}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif;line-height:1.95}
a{color:#075ba7;text-underline-offset:4px}a:hover{color:#a75800}.layout{max-width:1220px;margin:auto;display:grid;grid-template-columns:230px minmax(0,1fr);gap:28px;padding:36px 24px}
aside{position:sticky;top:28px;align-self:start;font-size:14px}aside h2{font-size:17px;margin-top:0}nav a{display:block;padding:7px 0;border-bottom:1px solid var(--border);text-decoration:none;line-height:1.65}.source-note{font-size:12px;color:var(--muted);overflow-wrap:anywhere}.translation-note{background:#fff8ea;border-left:4px solid var(--orange);padding:16px 22px;margin:0 0 26px;font-size:14px}.translation-note p{margin:0}
main{min-width:0}.pdf-page{background:var(--paper);padding:32px 46px;margin-bottom:24px;box-shadow:0 3px 18px #1f32400b;border:1px solid var(--border);border-radius:8px}.page-header{font-size:12px;color:var(--muted);border-bottom:1px solid var(--border);padding-bottom:12px;margin-bottom:24px;display:flex;justify-content:space-between;gap:20px}.page-header span:last-child{white-space:nowrap}.body p{margin:0 0 22px;text-align:justify;overflow-wrap:anywhere}.body h2{font-size:23px;line-height:1.6;margin:30px 0 20px;font-weight:700}.page-footer{text-align:center;color:var(--muted);font-size:12px;margin-top:30px}
.cover{border-top:4px solid var(--orange);padding:24px 0 0;min-height:630px;display:flex;flex-direction:column}.eyebrow{font-size:13px;color:var(--muted);letter-spacing:2px}.cover h1{font-size:38px;line-height:1.45;margin:85px 0 12px}.english-title{font-size:19px;line-height:1.6;color:var(--muted)}.author{font-size:17px;font-weight:600;margin-top:24px!important}.aws-logo{width:160px;max-width:100%;height:auto;align-self:flex-end;margin:70px 0 16px}.cover-footer{border-top:3px solid var(--orange);font-size:13px}.cover-footer p{font-size:11px!important;margin-top:6px!important}
figure{margin:26px 0 18px;text-align:center}figure img{width:auto;max-width:100%;height:auto;display:block;margin:auto;background:white}figcaption{color:var(--muted);font-size:13px;margin-top:12px;line-height:1.6}.table-scroll{overflow-x:auto;margin-bottom:26px}table{border-collapse:collapse;width:100%;font-size:13px;line-height:1.7}caption{text-align:left;font-size:12px;color:var(--muted);padding-bottom:8px}th,td{border:1px solid var(--border);padding:10px 12px;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#edf3f8}td:first-child{width:46%}
code{font-family:Consolas,"Microsoft YaHei",monospace;font-size:.91em;background:#eef2f6;padding:1px 4px;border-radius:3px}pre{background:#172433;color:#edf4ff;padding:20px;border-radius:6px;overflow:auto;line-height:1.7;font-size:13px;margin:22px 0}pre code{background:none;padding:0;white-space:pre;font-size:inherit}.continuation{font-size:12px;color:var(--muted);margin:10px 0 18px}
details{border-top:1px dashed var(--border);margin-top:24px;padding-top:12px}summary{font-size:13px;color:#075ba7;cursor:pointer}.original-page{width:100%;height:auto;display:block;margin-top:18px;border:1px solid var(--border)}.end{font-size:12px;color:var(--muted);text-align:center}
@media(max-width:920px){.layout{grid-template-columns:1fr;max-width:850px;padding:20px 16px}aside{position:static}nav{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}.source-note{margin-bottom:0}.pdf-page{padding:28px 30px}}
@media(max-width:520px){.layout{padding:14px 10px;gap:18px}.pdf-page{padding:22px 18px;border-radius:5px}.cover h1{font-size:29px;margin-top:58px}.cover{min-height:530px}.body h2{font-size:21px}.body p{font-size:15px;line-height:2}.page-header{font-size:10px;gap:12px}th,td{padding:8px}pre{padding:14px;font-size:12px}.translation-note{padding:12px 16px}nav{gap:0 15px}nav a{font-size:12px}}
@media print{body{background:white}.layout{display:block;padding:0;max-width:none}aside,.translation-note,details,.end{display:none}.pdf-page{border:0;box-shadow:none;border-radius:0;padding:10mm 5mm;break-before:page;margin:0}.pdf-page:first-of-type{break-before:auto}.cover{min-height:230mm}pre{white-space:pre-wrap;overflow:visible;background:#f1f4f8;color:#172433;font-size:10px}pre code{white-space:pre-wrap;overflow-wrap:anywhere}figure,table{break-inside:avoid}a{color:inherit;text-decoration:none}}
'''

navigation = [('cover','封面与版权'),('side-effects','重试与副作用'),('design','幂等 API 设计'),('semantics','语义等价与默认重试'),('late','迟到请求与标识符生命周期'),('parameters','相同 ID、不同参数'),('conclusion','结论')]
nav=''.join(f'<a href="#{key}">{label}</a>' for key,label in navigation)
sections=[]
for i,body in enumerate(pages,1):
    printed = '封面' if i == 1 else str(i-1)
    header = '' if i==1 else f'<header class="page-header"><span>通过幂等 API 实现安全重试</span><span>原文第 {i-1} 页</span></header>'
    footer = '' if i==1 else f'<footer class="page-footer">{i-1}</footer>'
    original=img(f'source-{i}.png',f'PDF 原始第 {i} 页，' + ('封面' if i==1 else f'印刷页码 {i-1}'),'original-page')
    sections.append(f'<section class="pdf-page" id="{"cover" if i==1 else "pdf-page-"+str(i)}" data-pdf-page="{i}">{header}<div class="body">{body}</div>{footer}<details><summary>展开原页核对 · PDF 第 {i} 页（{printed}）</summary>{original}</details></section>')

document='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Malcolm Featonby"><meta name="description" content="用户提供的 AWS PDF《Making retries safe with idempotent APIs》中文全文译本，含全部原图、图中文字翻译、代码与逐页原稿。"><title>通过幂等 API 实现安全重试 · 中文全文</title><style>''' + css + '''</style></head><body><div class="layout"><aside><h2>阅读目录</h2><nav>''' + nav + '''</nav><p class="source-note">来源：用户提供的 9 页 PDF<br>making-retries-safe-with-idempotent-apis-malcolm-featonby.pdf<br>作者：Malcolm Featonby</p></aside><main><div class="translation-note"><p><strong>译本说明（非原文）：</strong>按原 PDF 的封面及正文 1–8 页完整翻译。保留全部原图，并提供图中文字的中文对照；页眉、页码、版权及原文链接均保留。命令、API、JSON 字段和状态值保持英文，代码中的说明性文字译为中文。原文代码的省略号和跨页位置予以保留；长命令合并为一行显示。每页可展开原页核对。全部图片已内嵌，可离线阅读。</p></div>''' + ''.join(sections) + '''<p class="end">中文全文译本 · 原文版权归 Amazon Web Services, Inc. 和／或其关联公司所有。</p></main></div></body></html>'''
TARGET.write_text(document,encoding='utf-8')
print(TARGET)
print('Pages:',len(pages),'Images:',document.count('<img '),'Bytes:',TARGET.stat().st_size)
