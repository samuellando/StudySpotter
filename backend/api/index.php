<?php
// SQL connection.
$servername = "35.203.12.1:3306";
$username = "api";
$password = "GQ1$795aL";
$dbname = "goodquestion";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$CREATE = 0;

// CREATE the tables.
if ($CREATE) {
    $sql = "CREATE TABLE locations (
        id VARCHAR(225) PRIMARY KEY,
        lng FLOAT(53),
        lat FLOAT(53),
        name VARCHAR(255),
        avg INT(255),
        dsc VARCHAR(500)
    )";
    if ($conn->query($sql) === TRUE) {
       echo "Created locations table";
    } else {
        echo "Error creating table: " . $conn->error;
    }
    $sql = "CREATE TABLE mcgilltrotier (
        mac VARCHAR(225),
        last INT(255),
        power INT(255),
        label VARCHAR(255)
    )";
    if ($conn->query($sql) === TRUE) {
       echo "Created location table";
    } else {
        echo "Error creating table: " . $conn->error;
    }
}

// POST requests from the pi.
/*
$sql = "INSERT INTO locations (id, name, dsc, lng, lat, avg) VALUES ('mcgilltrotier', 'McGill Trotier Building', 'insert description here', 45.507572, -73.578976, 10);";
//$sql = "";
for ($i = 0; $i < 100; $i++) {
    $t = random_int(1573862400, 1573875180);
    $sql .= "INSERT INTO mcgilltrotier (mac, last, power, label) VALUES ('FFFFFFFF', $t, 5, 'First floor');";
}
if ($conn->multi_query($sql) === TRUE) {
    echo "New records created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}
*/
// GET requests from the frontend.
if (isset($_GET["location"])) {
    $loc = $_GET['location'];
    $sql = "SELECT name, dsc FROM locations WHERE id='$loc'";
    $result = $conn->query($sql);
    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $name = $row['name'];
        $dsc = $row['dsc'];
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
            while($row = $result->fetch_assoc()) {
                $n = array();
                $points;
                $avg;
                for ($i = 0; $i < 48; $i++) {
                    if ($i < 35)
                        $points[$i] = random_int(0, 100);
                    $avg[$i] = random_int(0, 100);
                }
                $n['data'] = $points;
                $n['avg'] = $avg;
                $data["labels"][$key] = $n;
            }
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
            $data["locations"][] = array('id'=>$row['id'], 'lat'=>$row['lat'], 'lng'=>$row['lng'], 'name'=>$row['name'], 'density'=>random_int(0, 100));
        }
    } else {
        $data["locations"] = "no data";
    }
    echo json_encode($data);
}

$conn->close();
?>
