<h1>Docker Microservices</h1>

<p>This project is based on microservice architecture using <b>Docker</b> and <b>Python Flask</b>. In this project we have several communication mechanisms, such as <b>gRPC</b>, <b>HTTP Rest</b> and <b>Publish Subscribe</b>.</p>
<br>

<ol>
  <li><b>To execute this project:</b></li>
  <li>Create a docker network- <i><b>docker network create mynet</b></i></li>
  <li>Change the variables of the configuration files of the different microservices.</li>
  <ol>
    <li><i>SELF_HOST_IP</i> - Is the ip of the machine in which it will execute the determined microservice.</li>
    <li><i>AUTH_HOST_IP</i>-Is the ip of the machine that is executing the Auth microservice.</li>
    <li><i>BOOKING_HOST_IP</i>-Is the ip of the machine that is executing the Booking microservice.</li>
    <li><i>RABBIT_HOST_IP</i>- Is the ip of the machine that is running the service of Rabbit Mq.</li>
  </ol>
  <li>For each microservice run <i><b>docker-compose up</i></b>.</li>
</ol>
  
