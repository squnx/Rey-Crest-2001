#!/usr/local/bin/perl 
#
############################################################################
#	EZ Form Mailer		Version 1.2
#
#	1.2	Corrected Y2K Compliance
#
#	1.1	Changed get_date to be Y2K compliant.
#
#	Copyright 1997, 1999 3rd Coast Technologies, LLC
#
#		http://www.3rdcoast.com
#		support@3rdcoast.com
#
#	This CGI script takes the data entered in an HTML form 
#	and sends it via e-mail to the specified location.
#
#	EZ Form Mailer is available for anyone to use or modify for no charge.
#	All we ask is that you leave this copyright notice in the script
#	and readme.txt file.  If someone asks where you got the script, 
#	refer them to 3rd Coast Technologies.
#
#	Selling or distributing this program without prior written approval
#	is forbidden. 
#
############################################################################
# 			Configuration Variables
#
#	The following variables are used to define how your form data
#	will be processed.  The data values can be defined here in the
#	script or optionally they can be sent from the form by hidden fields.
#	See the readme.txt file for information on using hidden fields.	 
#
############################################################################
#
# $SENDMAIL 	identifies the location of the send mail program on 
#		your server.  Verify this with your webmaster or isp.
#		******************************************************
#		***	This variable MUST be specified here and   *** 
#		***	cannot be sent using hidden fields.        ***
#		******************************************************
#
# @AUTHURLS 	identifies the URL's that are authorized to use this 
#		CGI Script.  Be sure to include all possible variations.
#		******************************************************
#		***	This variable MUST be specified here and   *** 
#		***	cannot be sent using hidden fields.        ***
#		******************************************************
#
# $TO 		the email address where the form data will be sent.
#
# $SUBJECT 	the text that will be used for the subject of the email.
#
# $REDIRECT 	identifies the page to be displayed to the user 
#           	after they submit the form.
#
# $SORT_TYPE 	defines the sort type for the form output.
#            	Options are 'alphabetic', 'field', or 'none'.
#
# @SORT_FIELDS 	If the $SORT_TYPE is 'field', enter the field names
#               in the desired print sequence.
#
#	When changing any of these values, be sure to include the single
#	quote marks around the values and the semi colon at the end of 
#	each statement.
#
############################################################################

$SENDMAIL = '/usr/lib/sendmail';

@AUTHURLS = ('www.reycrest.com','reycrest.com');

$TO       = 'quote@reycrest.com';

$SUBJECT  = 'Quote Request';

$REDIRECT = 'http://www.reycrest.com/confirm.html';

$SORT_TYPE = 'field';

@SORT_FIELDS = ('Name','Email');

############################################################################

# Check to make sure this script was called by an authorized URL(s)

	&check_url;

# Format Local Date/Time for Email Message Date

	&get_date;

# Reformat Form Contents

	&reformat_form_data;

# Send the form data to the recipient via e-mail

	&send_email;

# Redirect user to confirmation page

	print "Location: $REDIRECT\n\n";

	exit();

################################################################

sub check_url 
{
	if ($ENV{'HTTP_REFERER'}) 
	{
		foreach $AUTHURL (@AUTHURLS) 
		{
			if ($ENV{'HTTP_REFERER'} =~ /$AUTHURL/i) 
			{
				$check_url = '1';	   	
				last;
         		}
      		}
	}
	else 
	{
		$check_url = '1';
	}

	if ($check_url != 1) 
   	{
   		print "Content-type: text/html\n\n";
		print "<html>\n <head>\n  <title>Unauthorized URL Referrer - Access Denied</title>\n </head>\n";
      		print " <body>\n  <center>\n   <h1>Unauthorized URL Referrer - Access Denied</h1>\n  </center>\n";
      		print "The form that is trying to use this script resides at: \n";
      		print "$ENV{'HTTP_REFERER'}, which is not allowed to access this cgi script.<p>\n";
      		print "Sorry!\n";
      		print "</body></html>\n";
		exit;
	}

}

sub get_date 
{
   	@days = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
   	@months = ('January','February','March','April','May','June','July',
		'August','September','October','November','December');

   	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
   	if ($hour < 10) 
		{ $hour = "0$hour"; }
   	if ($min < 10) 
		{ $min = "0$min"; }
   	if ($sec < 10) 
		{ $sec = "0$sec"; }
	if ($year >= 100)
		{ $year = $year - 100; }
   	if ($year < 10) 
		{ $year = "0$year"; }
 	if ($year < 90) 
		{ $cent = "20"; }
	else
		{ $cent = "19"; }

   	$date = "$days[$wday], $months[$mon] $mday, $cent$year at $hour\:$min\:$sec";

	$mon = $mon + 1;
	if ($mon < 10) 
		{ $mon = "0$mon"; }
 	if ($mday < 10) 
		{ $mday = "0$mday"; }

	$dateShort = "$cent$year\-$mon\-$mday";
	$timeShort = "$hour\:$min\:$sec";

}

sub reformat_form_data
{
	if ($ENV{'REQUEST_METHOD'} eq 'POST') 
	{
      		# Get the input
      		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
      		# Split the name-value pairs
      		@pairs = split(/&/, $buffer);
   	}
   	else 
	{
  		print "Content-type: text/html\n\n";
      		print "<html>\n <head>\n  <title>Error: Request Method</title>\n </head>\n";
      		print "<body>\n <center>\n\n <h1>Error: Request Method</h1>\n  </center>\n\n";
      		print "The Request Method of the Form you submitted was not\n";
      		print "POST.  Please check the form, and make sure the\n";
      		print "method= statement is in upper case and is set to POST.\n";
      		print "<p><hr size=7 width=75%><p>\n";
      		print "<ul>\n";
      		print "<li><a href=\"$ENV{'HTTP_REFERER'}\">Back to the Submission Form</a>\n";
      		print "</ul>\n";
      		print "</body></html>\n";
		exit;
   	}
	foreach $pair (@pairs) 
	{
    		($name, $value) = split(/=/, $pair);
      		$name =~ tr/+/ /;
      		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
     		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/<!--(.|\n)*-->//g;
		if ($name eq 'email' || $name eq 'Name' && ($value)) 
		{
		      	$CONFIG{$name} = $value;
		}
		if ($name eq 'to_email' && ($value)) 
		{
			$TO = $value;
		}		
		elsif ($name eq 'subject' && ($value)) 
		{
			$SUBJECT = $value;
		}		
		elsif ($name eq 'redirect' && ($value)) 
		{
			$REDIRECT = $value;
		}		
		elsif ($name eq 'sort_type' && ($value)) 
		{
			$SORT_TYPE = $value;
		}				
		elsif ($name eq 'sort_fields' && ($value)) 
		{
			@SORT_FIELDS = split(/,/, $value);
		}		
		elsif ($FORM{$name} && ($value)) 
		{
			$FORM{$name} = "$FORM{$name}, $value";
	 	}
		elsif ($value) 
		{
      			$FORM{$name} = $value;
      		}
	}
}

sub send_email
{
# Build the 'from' address of the form: "name <email address>"

	$from_name=($CONFIG{'Name'} . " <" . $CONFIG{'email'} . "> ");

	open(MAIL,"|$SENDMAIL -t") || die "Can't open $mailprog!\n";

# Output the mail header

	print MAIL "To: $TO\r\n";
   	print MAIL "From: $from_name\r\n";
	print MAIL "Reply-To: $from_name\r\n";
	print MAIL "Subject: $SUBJECT\r\n\n";  

# Output the mail message header with the Local Date/Time

	print MAIL "---------------------------------------------------------------\n\n";
	print MAIL "   The following information was submitted by: \n";
	print MAIL "   $CONFIG{'Name'} on $date\n\n";
	print MAIL "---------------------------------------------------------------\n\n";

# Output the mail body
# Optionally Sort and Print the name and value pairs in FORM array

	if ($SORT_TYPE eq 'alphabetic') 
	{
      		foreach $key (sort keys %FORM) 
		{
         		print MAIL "$key: $FORM{$key}\n\n";
      		}
   	}
   	elsif ($SORT_TYPE eq 'field') 
	{
		foreach $SORT_FIELD (@SORT_FIELDS) 
		{
         		if ($FORM{$SORT_FIELD}) 
			{
            			print MAIL "$SORT_FIELD:  $FORM{$SORT_FIELD}\n\n";
			}
		}
	}
   	else 
	{
     		foreach $key (keys %FORM) 
		{
        		print MAIL "$key:  $FORM{$key}\n\n";
     		}
	}

# Output the mail footer

	print MAIL "<REMOTE HOST>    $ENV{'REMOTE_HOST'}\n";
	print MAIL "<REMOTE ADDRESS> $ENV{'REMOTE_ADDR'}\n";
	print MAIL "<USER AGENT>     $ENV{'HTTP_USER_AGENT'}\r\n";

# Close the pipe and send the mail

	close(MAIL);
}





