module default {
    type Assignment {
        required link owner -> User;
        required property title -> str;
        property deadline -> datetime; # check comptability with Python datetime
        property description -> str;
        multi link attachments -> Attachment {
            on target delete allow;
        }
        multi link works -> Work;
        property max_grade -> int16{default:=0; constraint min_value(0)}
    } 

    type Work {
        required link owner -> User;
        multi link attachments -> Attachment {
            on target delete allow;
        }
        property is_submitted -> bool{default:=false};
        property grade -> int16{default:=0;} # how to check if it is the default or not?
        
    }

    type Attachment {
        required property file -> bytes;
    }
}