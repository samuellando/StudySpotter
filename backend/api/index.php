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
    if (isset($_POST['name']) && isset($_POST['lat']) && isset($_POST['lng']) && isset($_POST['id']) && isset($_POST['dsc'])) {
        $name = $_POST['name'];
        $id = $_POST['id'];
        $lat = $_POST['lat'];
        $lng = $_POST['lng'];
        $sql = "CREATE TABLE $loc (
            mac VARCHAR(225),
            last INT(255),
            power INT(255),
            label VARCHAR(255)
        ); INSERT INTO locations (id, name, dsc, lat, lng, avg) VALUES ('$id', '$name', '$dsc', $lat, $lng, 0)";
    }
    // Import the new data.
    $json = $_SERVER['data'];
    $data = json_decode($json);
    $sql = "";
    for ($i = 0; $i < sizeof($data['macs']); $i++) {
        $mac = $data['macs'][$i];
        $last = $data['last'][$i];
        $power = $data['power'][$i];
        $sql .= "INSERT INTO $loc (mac, last, power, label) VALUES ($mac, $last, $power)";
    }
    if ($conn->query($sql) !== TRUE) {
       echo "{'status': 'bad'}";
       exit();
    }
    // Now compute the avg for the location.
    $sql = "SELECT avg locations WHERE id='$loc'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $avg = $row['avg'];
    }
    $avg = ($avg + sizeof($data['macs'])) / 2;
    $density = sizeof($data['macs']) / $avg * 100;
    $sql = "UPDATE locations SET avg='$avg', density='$density' WHERE id='$loc'";
    if ($conn->query($sql) === TRUE) {
       echo "{'status': 'good'}";
    } else {
       echo "{'status': 'bad'}";
    }
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
    $data = array('location'=>$loc, 'name'=>$name, 'dsc'=>$dsc);
    foreach ($labels as $key => $value) {
        $sql = "SELECT * FROM $loc where label='$key'";
        $result = $conn->query($sql);
        if ($result->num_rows > 0) {
            $points = array();
            $avgs = array();
            while($row = $result->fetch_assoc()) {
                $last = $row['last'];
                $block = intdiv((time() - intval($last)), (30*60));
                $points[$block] = $points[$block] + 1;
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