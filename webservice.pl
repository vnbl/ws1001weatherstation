use LWP::UserAgent;
use HTTP::Request::Common;

my $ua = LWP::UserAgent->new;
my $server_endpoint = "http://tiroleo.tech/WebApi/api/trabajosclima";

my $req = HTTP::Request->new(POST => $server_endpoint);
$req->header('content-type' => 'text/json');

my $post_data = '{ "FECHA_ALTA": "2018-01-19T11:11:22", "TEMPERATURA": 20.227, "HUMEDAD": 22294, "VIENTO": 032,"MAXIMA_VIENTO": 523,"LLUVIA": 3440,"SOL": 012,"BAROMETRO": 112312312,"ET": 1,"UV": 1, "ID": 1}';

$req->content($post_data);

print $req->as_string;

my $resp = $ua->request($req);
if ($resp->is_success) {
    my $message = $resp->decoded_content;
    print "Received reply: $message\n";
}
else {
    print "HTTP POST error code: ", $resp->code, "\n";
    print "HTTP POST error message: ", $resp->message, "\n";
}
