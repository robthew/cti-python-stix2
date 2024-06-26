import json

import stix2
from stix2.datastore.relational_db.relational_db import RelationalDBStore
import stix2.properties

store = RelationalDBStore(
    "postgresql://localhost/stix-data-sink",
    True,
    None,
    False,
    False
)

# Artifacts
basic_artifact_dict = {
    "type": "artifact",
    "spec_version": "2.1",
    "id": "artifact--cb37bcf8-9846-5ab4-8662-75c1bf6e63ee",
    "mime_type": "image/jpeg",
    "payload_bin": "VGhpcyBpcyBhIHBsYWNlaG9sZGVyIGZvciBhIHNhZmUgbWFsd2FyZSBiaW5hcnkh",
}

encrypted_artifact_dict = {
    "type": "artifact",
    "spec_version": "2.1",
    "id": "artifact--3857f78d-7d16-5092-99fe-ecff58408b02",
    "mime_type": "application/zip",
    "payload_bin": "VGhpcyBpcyBhIHBsYWNlaG9sZGVyIGZvciBhbiB1bnNhZmUgbWFsd2FyZSBiaW5hcnkh",
    "hashes": {
        "MD5": "6b885a1e1d42c0ca66e5f8a17e5a5d29",
        "SHA-256": "3eea3c4819e9d387ff6809f13dde5426b9466285b7d923016b2842a13eb2888b",
    },
    "encryption_algorithm": "mime-type-indicated",
    "decryption_key": "My voice is my passport",
}


def test_basic_artifact():
    artifact_stix_object = stix2.parse(basic_artifact_dict)
    store.add(artifact_stix_object)
    read_obj = json.loads(store.get(artifact_stix_object['id']).serialize())

    for attrib in basic_artifact_dict.keys():
        assert basic_artifact_dict[attrib] == read_obj[attrib]


def test_encrypted_artifact():
    artifact_stix_object = stix2.parse(encrypted_artifact_dict)
    store.add(artifact_stix_object)
    read_obj = json.loads(store.get(artifact_stix_object['id']).serialize())

    for attrib in encrypted_artifact_dict.keys():
        if attrib == 'hashes':  # TODO hashes are saved to separate table, functionality to retrieve is WIP
            continue
        assert encrypted_artifact_dict[attrib] == read_obj[attrib]


# Autonomous System
as_dict = {
    "type": "autonomous-system",
    "spec_version": "2.1",
    "id": "autonomous-system--f822c34b-98ae-597f-ade5-27dc241e8c74",
    "number": 15139,
    "name": "Slime Industries",
    "rir": "ARIN",
}


def test_autonomous_system():
    as_obj = stix2.parse(as_dict)
    store.add(as_obj)
    read_obj = json.loads(store.get(as_obj['id']).serialize())

    for attrib in as_dict.keys():
        assert as_dict[attrib] == read_obj[attrib]


# Directory
directory_dict = {
    "type": "directory",
    "spec_version": "2.1",
    "id": "directory--17c909b1-521d-545d-9094-1a08ddf46b05",
    "ctime": "2018-11-23T08:17:27.000Z",
    "mtime": "2018-11-23T08:17:27.000Z",
    "path": "C:\\Windows\\System32",
    "path_enc": "cGF0aF9lbmM",
    "contains_refs": [
        "directory--94c0a9b0-520d-545d-9094-1a08ddf46b05",
        "file--95c0a9b0-520d-545d-9094-1a08ddf46b05",
    ],
}


def test_directory():
    directory_obj = stix2.parse(directory_dict)
    store.add(directory_obj)
    read_obj = json.loads(store.get(directory_obj['id']).serialize())

    for attrib in directory_dict.keys():
        if attrib == "contains_refs":  # TODO remove skip once we can pull from table join
            continue
        if attrib == "ctime" or attrib == "mtime":  # convert both into stix2 date format for consistency
            assert stix2.utils.parse_into_datetime(directory_dict[attrib]) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert directory_dict[attrib] == read_obj[attrib]


# Domain Name
domain_name_dict = {
    "type": "domain-name",
    "spec_version": "2.1",
    "id": "domain-name--3c10e93f-798e-5a26-a0c1-08156efab7f5",
    "value": "example.com",
}


def test_domain_name():
    domain_name_obj = stix2.parse(domain_name_dict)
    store.add(domain_name_obj)
    read_obj = json.loads(store.get(domain_name_obj['id']).serialize())

    for attrib in domain_name_dict.keys():
        assert domain_name_dict[attrib] == read_obj[attrib]


# Email Address
email_addr_dict = {
    "type": "email-addr",
    "spec_version": "2.1",
    "id": "email-addr--2d77a846-6264-5d51-b586-e43822ea1ea3",
    "value": "john@example.com",
    "display_name": "John Doe",
    "belongs_to_ref": "user-account--0d5b424b-93b8-5cd8-ac36-306e1789d63c",
}


def test_email_addr():
    email_addr_stix_object = stix2.parse(email_addr_dict)
    store.add(email_addr_stix_object)
    read_obj = json.loads(store.get(email_addr_stix_object['id']).serialize())

    for attrib in email_addr_dict.keys():
        assert email_addr_dict[attrib] == read_obj[attrib]


# Email Message
email_msg_dict = {
    "type": "email-message",
    "spec_version": "2.1",
    "id": "email-message--8c57a381-2a17-5e61-8754-5ef96efb286c",
    "from_ref": "email-addr--9b7e29b3-fd8d-562e-b3f0-8fc8134f5dda",
    "sender_ref": "email-addr--9b7e29b3-fd8d-562e-b3f0-8fc8134f5eeb",
    "to_refs": ["email-addr--d1b3bf0c-f02a-51a1-8102-11aba7959868"],
    "cc_refs": [
        "email-addr--d2b3bf0c-f02a-51a1-8102-11aba7959868",
        "email-addr--d3b3bf0c-f02a-51a1-8102-11aba7959868",
    ],
    "bcc_refs": [
        "email-addr--d4b3bf0c-f02a-51a1-8102-11aba7959868",
        "email-addr--d5b3bf0c-f02a-51a1-8102-11aba7959868",
    ],
    "message_id": "message01",
    "is_multipart": False,
    "date": "2004-04-19T12:22:23.000Z",
    "subject": "Did you see this?",
    "received_lines": [
        "from mail.example.com ([198.51.100.3]) by smtp.gmail.com with ESMTPSA id \
        q23sm23309939wme.17.2016.07.19.07.20.32 (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 \
        bits=128/128); Tue, 19 Jul 2016 07:20:40 -0700 (PDT)",
    ],
    "additional_header_fields": {
        "Reply-To": [
            "steve@example.com",
            "jane@example.com",
        ],
    },
    "body": "message body",
    "raw_email_ref": "artifact--cb37bcf8-9846-5ab4-8662-75c1bf6e63ee",
}

multipart_email_msg_dict = {
    "type": "email-message",
    "spec_version": "2.1",
    "id": "email-message--ef9b4b7f-14c8-5955-8065-020e0316b559",
    "is_multipart": True,
    "received_lines": [
        "from mail.example.com ([198.51.100.3]) by smtp.gmail.com with ESMTPSA id \
        q23sm23309939wme.17.2016.07.19.07.20.32 (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 \
        bits=128/128); Tue, 19 Jul 2016 07:20:40 -0700 (PDT)",
    ],
    "content_type": "multipart/mixed",
    "date": "2016-06-19T14:20:40.000Z",
    "from_ref": "email-addr--89f52ea8-d6ef-51e9-8fce-6a29236436ed",
    "to_refs": ["email-addr--d1b3bf0c-f02a-51a1-8102-11aba7959868"],
    "cc_refs": ["email-addr--e4ee5301-b52d-59cd-a8fa-8036738c7194"],
    "subject": "Check out this picture of a cat!",
    "additional_header_fields": {
        "Content-Disposition": "inline",
        "X-Mailer": "Mutt/1.5.23",
        "X-Originating-IP": "198.51.100.3",
    },
    "body_multipart": [
        {
            "content_type": "text/plain; charset=utf-8",
            "content_disposition": "inline",
            "body": "Cats are funny!",
        },
        {
            "content_type": "image/png",
            "content_disposition": "attachment; filename=\"tabby.png\"",
            "body_raw_ref": "artifact--4cce66f8-6eaa-53cb-85d5-3a85fca3a6c5",
        },
        {
            "content_type": "application/zip",
            "content_disposition": "attachment; filename=\"tabby_pics.zip\"",
            "body_raw_ref": "file--6ce09d9c-0ad3-5ebf-900c-e3cb288955b5",
        },
    ],
}


def test_email_msg():
    email_msg_stix_object = stix2.parse(email_msg_dict)
    store.add(email_msg_stix_object)
    read_obj = json.loads(store.get(email_msg_stix_object['id']).serialize())

    for attrib in email_msg_dict.keys():
        if attrib == "to_refs" or attrib == "cc_refs" or attrib == "bcc_refs" \
                or attrib == "additional_header_fields":  # join multiple tables not implemented yet
            continue
        if attrib == "date":
            assert stix2.utils.parse_into_datetime(email_msg_dict[attrib]) == stix2.utils.parse_into_datetime(
                read_obj[attrib],
            )
            continue
        assert email_msg_dict[attrib] == read_obj[attrib]


def test_multipart_email_msg():
    multipart_email_msg_stix_object = stix2.parse(multipart_email_msg_dict)
    store.add(multipart_email_msg_stix_object)
    read_obj = json.loads(store.get(multipart_email_msg_stix_object['id']).serialize())

    for attrib in multipart_email_msg_dict.keys():
        if attrib == "to_refs" or attrib == "cc_refs" or attrib == "bcc_refs" \
                or attrib == "additional_header_fields" or attrib == "body_multipart":  # join multiple tables not implemented yet
            continue
        if attrib == "date":
            assert stix2.utils.parse_into_datetime(multipart_email_msg_dict[attrib]) == stix2.utils.parse_into_datetime(
                read_obj[attrib],
            )
            continue
        assert multipart_email_msg_dict[attrib] == read_obj[attrib]


# File
# errors when adding magic_number_hex to store, so ignoring for now
file_dict = {
    "type": "file",
    "spec_version": "2.1",
    "id": "file--66156fad-2a7d-5237-bbb4-ba1912887cfe",
    "hashes": {
        "SHA-256": "ceafbfd424be2ca4a5f0402cae090dda2fb0526cf521b60b60077c0f622b285a",
    },
    "parent_directory_ref": "directory--93c0a9b0-520d-545d-9094-1a08ddf46b05",
    "name": "qwerty.dll",
    "size": 25536,
    "name_enc": "windows-1252",
    "mime_type": "application/msword",
    "ctime": "2018-11-23T08:17:27.000Z",
    "mtime": "2018-11-23T08:17:27.000Z",
    "atime": "2018-11-23T08:17:27.000Z",
    "contains_refs": [
        "file--77156fad-2a0d-5237-bba4-ba1912887cfe",
    ],
    "content_ref": "artifact--cb37bcf8-9846-5ab4-8662-75c1bf6e63ee",
}


def test_file():
    file_stix_object = stix2.parse(file_dict)
    store.add(file_stix_object)
    read_obj = json.loads(store.get(file_stix_object['id']).serialize())

    for attrib in file_dict.keys():
        if attrib == "contains_refs" or attrib == "hashes":  # join multiple tables not implemented yet
            continue
        if attrib == "ctime" or attrib == "mtime" or attrib == "atime":
            assert stix2.utils.parse_into_datetime(file_dict[attrib]) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert file_dict[attrib] == read_obj[attrib]


# ipv4 ipv6
ipv4_dict = {
    "type": "ipv4-addr",
    "spec_version": "2.1",
    "id": "ipv4-addr--ff26c255-6336-5bc5-b98d-13d6226742dd",
    "value": "198.51.100.3",
}

ipv6_dict = {
    "type": "ipv6-addr",
    "spec_version": "2.1",
    "id": "ipv6-addr--1e61d36c-a26c-53b7-a80f-2a00161c96b1",
    "value": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
}


def test_ipv4():
    ipv4_stix_object = stix2.parse(ipv4_dict)
    store.add(ipv4_stix_object)
    read_obj = store.get(ipv4_stix_object['id'])

    for attrib in ipv4_dict.keys():
        assert ipv4_dict[attrib] == read_obj[attrib]


def test_ipv6():
    ipv6_stix_object = stix2.parse(ipv6_dict)
    store.add(ipv6_stix_object)
    read_obj = store.get(ipv6_stix_object['id'])

    for attrib in ipv6_dict.keys():
        assert ipv6_dict[attrib] == read_obj[attrib]


# Mutex
mutex_dict = {
    "type": "mutex",
    "spec_version": "2.1",
    "id": "mutex--fba44954-d4e4-5d3b-814c-2b17dd8de300",
    "name": "__CLEANSWEEP__",
}


def test_mutex():
    mutex_stix_object = stix2.parse(mutex_dict)
    store.add(mutex_stix_object)
    read_obj = store.get(mutex_stix_object['id'])

    for attrib in mutex_dict.keys():
        assert mutex_dict[attrib] == read_obj[attrib]


# Network Traffic
# ipfix property results in a unconsumed value error with the store add
network_traffic_dict = {
    "type": "network-traffic",
    "spec_version": "2.1",
    "id": "network-traffic--631d7bb1-6bbc-53a6-a6d4-f3c2d35c2734",
    "src_ref": "ipv4-addr--4d22aae0-2bf9-5427-8819-e4f6abf20a53",
    "dst_ref": "ipv4-addr--03b708d9-7761-5523-ab75-5ea096294a68",
    "start": "2018-11-23T08:17:27.000Z",
    "end": "2018-11-23T08:18:27.000Z",
    "is_active": False,
    "src_port": 1000,
    "dst_port": 1000,
    "protocols": [
        "ipv4",
        "tcp",
    ],
    "src_byte_count": 147600,
    "dst_byte_count": 147600,
    "src_packets": 100,
    "dst_packets": 100,
    "src_payload_ref": "artifact--3857f78d-7d16-5092-99fe-ecff58408b02",
    "dst_payload_ref": "artifact--3857f78d-7d16-5092-99fe-ecff58408b03",
    "encapsulates_refs": [
        "network-traffic--53e0bf48-2eee-5c03-8bde-ed7049d2c0a3",
        "network-traffic--53e0bf48-2eee-5c03-8bde-ed7049d2c0a4",
    ],
    "encapsulated_by_ref": "network-traffic--53e0bf48-2eee-5c03-8bde-ed7049d2c0a5",
}


def test_network_traffic():
    network_traffic_stix_object = stix2.parse(network_traffic_dict)
    store.add(network_traffic_stix_object)
    read_obj = store.get(network_traffic_stix_object['id'])

    for attrib in network_traffic_dict.keys():
        if attrib == "encapsulates_refs":  # multiple table join not implemented
            continue
        if attrib == "start" or attrib == "end":
            assert stix2.utils.parse_into_datetime(network_traffic_dict[attrib]) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert network_traffic_dict[attrib] == read_obj[attrib]


# Process
process_dict = {
    "type": "process",
    "spec_version": "2.1",
    "id": "process--f52a906a-0dfc-40bd-92f1-e7778ead38a9",
    "is_hidden": False,
    "pid": 1221,
    "created_time": "2016-01-20T14:11:25.55Z",
    "cwd": "/tmp/",
    "environment_variables": {
        "ENVTEST": "/path/to/bin",
    },
    "command_line": "./gedit-bin --new-window",
    "opened_connection_refs": [
        "network-traffic--53e0bf48-2eee-5c03-8bde-ed7049d2c0a3",
    ],
    "creator_user_ref": "user-account--cb37bcf8-9846-5ab4-8662-75c1bf6e63ee",
    "image_ref": "file--e04f22d1-be2c-59de-add8-10f61d15fe20",
    "parent_ref": "process--f52a906a-1dfc-40bd-92f1-e7778ead38a9",
    "child_refs": [
        "process--ff2a906a-1dfc-40bd-92f1-e7778ead38a9",
        "process--fe2a906a-1dfc-40bd-92f1-e7778ead38a9",
    ],
}


def test_process():
    process_stix_object = stix2.parse(process_dict)
    store.add(process_stix_object)
    read_obj = json.loads(store.get(process_stix_object['id']).serialize())

    for attrib in process_dict.keys():
        if attrib == "child_refs" or attrib == "opened_connection_refs" or attrib == "environment_variables":
            # join multiple tables not implemented yet
            continue
        if attrib == "created_time":
            assert stix2.utils.parse_into_datetime(process_dict[attrib]) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert process_dict[attrib] == read_obj[attrib]


# Software
software_dict = {
    "type": "software",
    "spec_version": "2.1",
    "id": "software--a1827f6d-ca53-5605-9e93-4316cd22a00a",
    "name": "Word",
    "cpe": "cpe:2.3:a:microsoft:word:2000:*:*:*:*:*:*:*",
    "version": "2002",
    "vendor": "Microsoft",
}


def test_software():
    software_stix_object = stix2.parse(software_dict)
    store.add(software_stix_object)
    read_obj = json.loads(store.get(software_stix_object['id']).serialize())

    for attrib in software_dict.keys():
        assert software_dict[attrib] == read_obj[attrib]


# URL
url_dict = {
    "type": "url",
    "id": "url--a5477287-23ac-5971-a010-5c287877fa60",
    "value": "https://example.com/research/index.html",
}


def test_url():
    url_stix_object = stix2.parse(url_dict)
    store.add(url_stix_object)
    read_obj = json.loads(store.get(url_stix_object['id']).serialize())

    for attrib in url_dict.keys():
        assert url_dict[attrib] == read_obj[attrib]


# User Account
user_account_dict = {
    "type": "user-account",
    "spec_version": "2.1",
    "id": "user-account--0d5b424b-93b8-5cd8-ac36-306e1789d63c",
    "user_id": "1001",
    "credential": "password",
    "account_login": "jdoe",
    "account_type": "unix",
    "display_name": "John Doe",
    "is_service_account": False,
    "is_privileged": False,
    "can_escalate_privs": True,
    "is_disabled": False,
    "account_created": "2016-01-20T12:31:12Z",
    "account_expires": "2018-01-20T12:31:12Z",
    "credential_last_changed": "2016-01-20T14:27:43Z",
    "account_first_login": "2016-01-20T14:26:07Z",
    "account_last_login": "2016-07-22T16:08:28Z",
}


def test_user_account():
    user_account_stix_object = stix2.parse(user_account_dict)
    store.add(user_account_stix_object)
    read_obj = json.loads(store.get(user_account_stix_object['id']).serialize())

    for attrib in user_account_dict.keys():
        if attrib == "account_created" or attrib == "account_expires" \
                or attrib == "credential_last_changed" or attrib == "account_first_login" \
                or attrib == "account_last_login":
            assert stix2.utils.parse_into_datetime(user_account_dict[attrib]) == stix2.utils.parse_into_datetime(
                read_obj[attrib],
            )
            continue
        assert user_account_dict[attrib] == read_obj[attrib]


# Windows Registry
windows_registry_dict = {
    "type": "windows-registry-key",
    "spec_version": "2.1",
    "id": "windows-registry-key--2ba37ae7-2745-5082-9dfd-9486dad41016",
    "key": "hkey_local_machine\\system\\bar\\foo",
    "values": [
        {
            "name": "Foo",
            "data": "qwerty",
            "data_type": "REG_SZ",
        },
        {
            "name": "Bar",
            "data": "42",
            "data_type": "REG_DWORD",
        },
    ],
    "modified_time": "2018-01-20T12:31:12Z",
    "creator_user_ref": "user-account--0d5b424b-93b8-5cd8-ac36-306e1789d63c",
    "number_of_subkeys": 2,
}


def test_windows_registry():
    windows_registry_stix_object = stix2.parse(windows_registry_dict)
    store.add(windows_registry_stix_object)
    read_obj = json.loads(store.get(windows_registry_stix_object['id']).serialize())

    for attrib in windows_registry_dict.keys():
        if attrib == "values":  # skip multiple table join
            continue
        if attrib == "modified_time":
            assert stix2.utils.parse_into_datetime(windows_registry_dict[attrib]) == stix2.utils.parse_into_datetime(
                read_obj[attrib],
            )
            continue
        assert windows_registry_dict[attrib] == read_obj[attrib]


# x509 Certificate
basic_x509_certificate_dict = {
    "type": "x509-certificate",
    "spec_version": "2.1",
    "id": "x509-certificate--463d7b2a-8516-5a50-a3d7-6f801465d5de",
    "issuer": "C=ZA, ST=Western Cape, L=Cape Town, O=Thawte Consulting cc, OU=Certification  \
    Services Division, CN=Thawte Server CA/emailAddress=server-certs@thawte.com",
    "validity_not_before": "2016-03-12T12:00:00Z",
    "validity_not_after": "2016-08-21T12:00:00Z",
    "subject": "C=US, ST=Maryland, L=Pasadena, O=Brent Baccala, OU=FreeSoft, \
    CN=www.freesoft.org/emailAddress=baccala@freesoft.org",
    "serial_number": "36:f7:d4:32:f4:ab:70:ea:d3:ce:98:6e:ea:99:93:49:32:0a:b7:06",
}

extensions_x509_certificate_dict = {
    "type": "x509-certificate",
    "spec_version": "2.1",
    "id": "x509-certificate--b595eaf0-0b28-5dad-9e8e-0fab9c1facc9",
    "issuer": "C=ZA, ST=Western Cape, L=Cape Town, O=Thawte Consulting cc, OU=Certification \
    Services Division, CN=Thawte Server CA/emailAddress=server-certs@thawte.com",
    "validity_not_before": "2016-03-12T12:00:00Z",
    "validity_not_after": "2016-08-21T12:00:00Z",
    "subject": "C=US, ST=Maryland, L=Pasadena, O=Brent Baccala, OU=FreeSoft, \
    CN=www.freesoft.org/emailAddress=baccala@freesoft.org",
    "serial_number": "02:08:87:83:f2:13:58:1f:79:52:1e:66:90:0a:02:24:c9:6b:c7:dc",
    "x509_v3_extensions": {
        "basic_constraints": "critical,CA:TRUE, pathlen:0",
        "name_constraints": "permitted;IP:192.168.0.0/255.255.0.0",
        "policy_constraints": "requireExplicitPolicy:3",
        "key_usage": "critical, keyCertSign",
        "extended_key_usage": "critical,codeSigning,1.2.3.4",
        "subject_key_identifier": "hash",
        "authority_key_identifier": "keyid,issuer",
        "subject_alternative_name": "email:my@other.address,RID:1.2.3.4",
        "issuer_alternative_name": "issuer:copy",
        "crl_distribution_points": "URI:http://myhost.com/myca.crl",
        "inhibit_any_policy": "2",
        "private_key_usage_period_not_before": "2016-03-12T12:00:00Z",
        "private_key_usage_period_not_after": "2018-03-12T12:00:00Z",
        "certificate_policies": "1.2.4.5, 1.1.3.4",
    },
}


def test_basic_x509_certificate():
    basic_x509_certificate_stix_object = stix2.parse(basic_x509_certificate_dict)
    store.add(basic_x509_certificate_stix_object)
    read_obj = json.loads(store.get(basic_x509_certificate_stix_object['id']).serialize())

    for attrib in basic_x509_certificate_dict.keys():
        if attrib == "validity_not_before" or attrib == "validity_not_after":
            assert stix2.utils.parse_into_datetime(
                basic_x509_certificate_dict[attrib],
            ) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert basic_x509_certificate_dict[attrib] == read_obj[attrib]


def test_x509_certificate_with_extensions():
    extensions_x509_certificate_stix_object = stix2.parse(extensions_x509_certificate_dict)
    store.add(extensions_x509_certificate_stix_object)
    read_obj = json.loads(store.get(extensions_x509_certificate_stix_object['id']).serialize())

    for attrib in extensions_x509_certificate_dict.keys():
        if attrib == "x509_v3_extensions":  # skipping multi-table join
            continue
        if attrib == "validity_not_before" or attrib == "validity_not_after":
            assert stix2.utils.parse_into_datetime(
                extensions_x509_certificate_dict[attrib],
            ) == stix2.utils.parse_into_datetime(read_obj[attrib])
            continue
        assert extensions_x509_certificate_dict[attrib] == read_obj[attrib]
