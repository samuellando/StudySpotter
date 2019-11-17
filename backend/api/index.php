<?php
// SQL connection.
$servername = "35.203.12.1:3306";
$username = "api";
$password = "GQ1$795aL";
$dbname = "goodquestion";

// Create connection.
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection.
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// POST requests from the pi.
if (isset($_POST['location']) && isset($_POST['label'])) {
    // Create the tables if needed.
    $loc = $_POST['location'];
    $lab = $_POST['label'];
    if (isset($_POST['name']) && isset($_POST['lat']) && isset($_POST['lng']) && isset($_POST['dsc'])) {
        $name = $_POST['name'];
        $lat = $_POST['lat'];
        $lng = $_POST['lng'];
        $dsc = $_POST['dsc'];
        $sql = "CREATE TABLE $loc (
            mac VARCHAR(225),
            last INT(255),
            power INT(255),
            label VARCHAR(255)
        );";
        $conn->query($sql);
        $sql = "INSERT INTO locations (id, name, dsc, lat, lng, avg) VALUES ('$loc', '$name', '$dsc', $lat, $lng, -1)";
        $conn->query($sql);
    }
    // Import the new data.
    $json = $_POST['data'];
    $data = json_decode($json, TRUE);
    $sql = "INSERT INTO $loc (mac, last, power, label) VALUES ";
    for ($i = 0; $i < sizeof($data['macs']); $i++) {
        if ($i > 0) $sql .= ", ";
        $mac = $data['macs'][$i];
        $last = $data['last'][$i];
        $power = $data['power'][$i];
        $sql .= "('$mac', $last, $power, '$lab')";
    }
    if ($i > 0 && $conn->query($sql) !== TRUE) {
       echo '{"status": "bad"}';
       exit();
    }
    // Now compute the avg for the location.
    $sql = "SELECT avg FROM locations WHERE id='$loc'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $avg = $row['avg'];
    }
    $min = $data['last'][0];
    $max = $data['last'][0];
    for ($i = 1; $i < sizeof($data['last']); $i++) {
        if ($data['last'][$i] > $max) $max = $data['last'][$i];
        if ($data['last'][$i] < $min) $min = $data['last'][$i];
    }
    if ($avg != -1)
        $avg = intdiv(($avg + sizeof($data['macs'])), 2);
    else
        $avg = sizeof($data['macs']);
    $density = sizeof($data['macs']) / ($avg*2) * 100;
    $sql = "UPDATE locations SET avg='$avg', density='$density' WHERE id='$loc'";
    if ($conn->query($sql) === TRUE) {
       echo '{"status": "good"}';
    } else {
       echo '{"status": "bad"}';
    }
    exit();
}

// GET requests from the frontend.
if (isset($_GET["location"])) {
    $loc = $_GET['location'];
    $sql = "SELECT name, dsc, avg FROM locations WHERE id='$loc'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $name = $row['name'];
        $dsc = $row['dsc'];
        $avg = $row['avg'];
    } else {
        $name = "no data";
        $dsc = "no data";
    }
    $sql = "SELECT * FROM $loc";
    $result = $conn->query($sql);
    $labels = array();
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $labels[$row['label']] = 1;
        }
    }
    $data = array('id'=>$loc, 'name'=>$name, 'dsc'=>$dsc);
    $start = strtotime("today", $timestamp) - 5*3600;
    foreach ($labels as $key => $value) {
        $sql = "SELECT * FROM $loc WHERE label='$key' AND last>'$start'";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            $counts = array();
            while($row = $result->fetch_assoc()) {
                $last = $row['last'];
                $block = intdiv(((time() - 5*3600) - intval($last)), (30*60));
                $counts[$block] = $counts[$block] + 1;
            }
            $points = array();
            $avgs = array();
            foreach ($counts as $k => $v) {
               $points[] = $v;
            }
            while (sizeof($points) < 48) {
                $points[] = 0;
            }
            for ($i = 0; $i < 48; $i++) {
               $avgs[$i] = $avg; 
            }
            $n = array();
            $n['data'] = $points;
            $n['avg'] = $avgs;
            $data["labels"][$key] = $n;
        } else {
            $data["labels"][] = "no data";
        }
    }
    echo json_encode($data);
} else {
    $sql = "SELECT * FROM locations";
    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $data["locations"][] = array('id'=>$row['id'], 'lat'=>$row['lat'], 'lng'=>$row['lng'], 'name'=>$row['name'], 'density'=>$row['density']);
        }
    } else {
        $data["locations"] = "no data";
    }
    echo json_encode($data);
}

$conn->close();
?>