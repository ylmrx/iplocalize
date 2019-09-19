use MaxMind::DB::Writer::Tree;

my %types = (
    country => 'map',
    iso_code => 'utf8_string',
);

my $tree = MaxMind::DB::Writer::Tree->new(
    ip_version            => 6,
    record_size           => 24,
    database_type         => 'GeoIP2-City',
    languages             => ['en'],
    description           => { en => 'Example mmdb file' },
    map_key_type_callback => sub { $types{ $_[0] } },
);

$tree->insert_network( '1.2.3.0/24', { country => { iso_code => 'PC' }, },);
open my $fh, '>:raw', './fake-data.mmdb';
$tree->write_tree($fh);
