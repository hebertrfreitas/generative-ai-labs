#!/bin/sh
echo "Waiting 10 seconds  to add hosts"
sleep 10
for i in `seq 1 70`;do
    var=$(nebula-console -addr graphd -port 9669 -u root -p nebula -e 'ADD HOSTS "storaged0":9779');
    if [[ $? == 0 ]];then
        break;
    fi;
    echo "status for add hosts: ${var}" 
    sleep 1;
    echo "retry to add hosts.";
done;

is_storage_online(){
    check=$(nebula-console -addr graphd -port 9669 -u root -p nebula -e 'SHOW HOSTS' | grep "storaged0" | awk -F'|' '{print $4}' | grep "ONLINE" );
    return $?
}

while ! is_storage_online; do
  echo "Waiting for storage to come online..."
  sleep 1 # Wait for 1 second before checking again
done

echo "hosts:"
nebula-console -addr graphd -port 9669 -u root -p nebula -e 'SHOW HOSTS'
echo "Starting setup space";
nebula-console -addr graphd -port 9669 -u root -p nebula -e 'CREATE SPACE IF NOT EXISTS tomb_raider(vid_type=FIXED_STRING(256))';
echo "Waiting 30 seconds"; 
sleep 20;
echo "Creating tags, edges and indexes";
nebula-console -addr graphd -port 9669 -u root -p nebula -e 'USE tomb_raider; CREATE TAG IF NOT EXISTS entity(name string);';
nebula-console -addr graphd -port 9669 -u root -p nebula -e 'USE tomb_raider; CREATE EDGE IF NOT EXISTS relationship(relationship string);';
nebula-console -addr graphd -port 9669 -u root -p nebula -e 'USE tomb_raider; CREATE TAG INDEX IF NOT EXISTS entity_index ON entity(name(256));';
echo "Space setup end";

tail -f /dev/null;

