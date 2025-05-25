<?php
// echo "Today <font color=red><b>is</b></font> " . date("Y-m-d H:i:s") . "<br>";
// get the parameter from URL
$cmd = $_REQUEST["cmd"];
// $cmd = "list";
exec("echo \"".$cmd."\" | nc -q0 $(ip route | awk '/default/ {print $9}') 1234", $o);
//exec("echo \"list\" | nc -q0 192.168.1.108 1234", $o);
echo $o[0];
