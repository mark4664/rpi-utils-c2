<html>
<head>
<title>Raspberry Pi IP addresses</title>
</head>
<body style="font-family: Sans-Serif;">
<?php 

echo "<h2>rpi-utils</h2>\n";
echo "<h3>Raspberry Pi IP addresses</h3>\n"; 

$column_colours = ["lightgrey","lightcyan","peachpuff","lightblue","lightgreen","khaki"];
echo '<table style="text-align:center; border="0">';
echo "\n";
echo '<tr>';
echo "\n";
echo '<th width="20%" bgcolor= "'.$column_colours[0].'">Machine name</th>';
echo "\n";
echo '<th width="15%" bgcolor= "'.$column_colours[1].'">Wired</th>';
echo "\n";
echo '<th width="15%" bgcolor= "'.$column_colours[2].'">Wireless</th>';
echo "\n";
echo '<th width="15%" bgcolor= "'.$column_colours[3].'">Date</th>';
echo "\n";
echo '<th width="15%" bgcolor= "'.$column_colours[4].'">Time</th>';
echo "\n";
echo '<th width="20%" bgcolor= "'.$column_colours[5].'">Router IP address</th>';
echo "\n";
echo '</tr>';
echo "\n";


$rpi_files = glob("*.txt");
# print_r($rpi_files);
foreach ($rpi_files as  $key => $rpi_file) {
   # echo  $key ." =>" .$rpi_file;
   if ($rpi_file[10]!='p') {
   $fh = fopen($rpi_file, "r") or die("Unable to open file!");
   $fcontents = fread($fh,filesize($rpi_file));
   $fitems = explode("\n",$fcontents);
                echo "<tr>\n";
                echo '<td bgcolor= "'.$column_colours[0].'">'.$fitems[0]."</td>\n";
                echo '<td bgcolor= "'.$column_colours[1].'">'.str_replace("eth0: ","",$fitems[3])."</td>\n";
                echo '<td bgcolor= "'.$column_colours[2].'">'.str_replace("wlan0: ","",$fitems[4])."</td>\n";
                echo '<td bgcolor= "'.$column_colours[3].'">'.$fitems[1]."</td>\n";
                echo '<td bgcolor= "'.$column_colours[4].'">'.$fitems[2]."</td>\n";
                echo '<td bgcolor= "'.$column_colours[5].'">';
                if (count($fitems)==6) 
                {
                    echo($fitems[5]);
                } 
                else
                {
                    echo 'not known';
                };
                echo "</td>\n";
                echo "</tr>\n";
   fclose($fh);
   }
}
?>
</table>
</body>
</html>
