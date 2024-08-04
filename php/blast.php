<?php
header('Content-Type: application/json');
require_once("/var/www/html/payplus/connection.php");
require_once(__DIR__ . "/utils.php");

if ($_SERVER["REQUEST_METHOD"] !== "GET") {
    http_response_code(400);
    exit(json_encode(["status" => true, "message" => "Method not allowed"]));
}

$validate_response = validate_params($_GET);
if (!$validate_response["status"]) {
    http_response_code(400);
    exit(json_encode($validate_response));
}

if (mysqli_connect_error($con5)) {
    exit(json_encode(["status" => false, "message" => "Database connection failed"]));
}

$sql = get_query($validate_response);
$result = mysqli_query($con5, $sql);

if (!$result) {
    http_response_code(412);
    exit(json_encode(["status" => false, "data" => mysqli_error($con5)]));
}

$data = [];
while ($row = mysqli_fetch_assoc($result)) {
    $data[] = $row;
}


echo json_encode(["status" => true, "data" => $data]);
mysqli_close($con);
