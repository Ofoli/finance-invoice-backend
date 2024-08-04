<?php
function get_query(array $params): string
{
    $id = $params['id'];
    $type = $params["type"];
    $end_date = $params["end_date"];
    $start_date = $params["start_date"];

    $user_key = $type === "reseller" ? "users.reseller_id" : "users.id";

    return  "SELECT jobs.job_id as jobid, 
        jobs.time_created as sent_date, 
        users.display_username as username,
        senders.text AS sender,
        jobs.total_pages_count as pages_count, 
        jobs.total_SMS_count as total_sms, 
        jobs.message as message, 
        jobs.encryption_key as ekey
    FROM  sms_backend.userportal_senderid senders
    INNER JOIN sms_backend.userportal_smsjob jobs ON senders.id = jobs.sender_id_id
    INNER JOIN sms_backend.userportal_userprofile users ON jobs.user_id = users.id
    WHERE jobs.time_created >= '$start_date' 
        AND jobs.time_created < '$end_date' 
        AND jobs.job_id NOT LIKE 'api%' 
        AND jobs.status = '4' 
        AND $user_key = $id";
}

function validate_params(array $request): array
{
    $id = $request['id'] ? $request['id'] : "";
    $type = $request['type'] ? $request['type'] : "";
    $end_date = $request["end_date"] ? $request["end_date"] : "";
    $start_date = $request["start_date"] ? $request["start_date"] : "";

    $response = ["status" => false, "data" => null];

    if (!$id || !$type || !$start_date || !$end_date) {
        $response["data"] = "Missing id, type, start_date or end_date parameter";
        return $response;
    }

    if (!in_array($type, ["user", "reseller"])) {
        $response["data"] = "Invalid type provided";
        return $response;
    }

    if (new DateTime($start_date) > new DateTime($end_date)) {
        $response["data"] = "start_date cannot be greater than end_date";
        return $response;
    }

    $response["status"] = true;
    $response["data"] = [
        "id" => $id,
        "type" => $type,
        "start_date" => $start_date,
        "end_date" => $end_date
    ];

    return $response;
}
