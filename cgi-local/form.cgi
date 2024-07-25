#!/usr/bin/perl5
push (@INC, '/cgi-bin');
require ('cgi-lib.pl');

# This should match the mail program on your system.
$mailprog = '/usr/sbin/sendmail';

# This should be set to the username or alias that processes the
# requests


#------ Change 1 ----- Replace the name and domain with your actual name and domainname


$recipient = "corydana\@pacbell.net";


# Print out a content-type for HTTP/1.0 compatibility
print "Content-type: text/html\n\n";

# Print a title and initial heading
print "<Head><Title>User Email Info</Title></Head>";

&ReadParse;

#------ Change 2 ----- Replace the login with your actual login name

open (MAIL, "|$mailprog $recipient") || die "Unable to send request\nPlease send e-mail to quote\@reycrest.com, Thank you\n";
#open (MAIL, ">test") || die "Cannot open STDOUT: $!\n"; 
print MAIL "Reply-to: $in{'email'}\n";
print MAIL "Subject: User Email Information!\n";
print MAIL "\n\n";
#print "*$#in_key\n";
foreach $i (0 .. $#in_key){
#print "$in_key[$i] = $in_val[$i], i = $i <p>";
print MAIL "$in_key[$i] = $in_val[$i]\n"; 
}
print MAIL "-----------------------------------------------\n";
close (MAIL);

# ------Change 3-------- (Optional): You can replace some of the words below.
# You may want to not change it first and test it online. DO NO ALTER PRINT STATEMENT OR THE "EOT AT THE BOTTOM OF THIS PAGE. 

print <<"EOT";
 
                   



	



EOT


