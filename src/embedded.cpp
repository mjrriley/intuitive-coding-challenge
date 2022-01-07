#include "embedded.h"
#include <unistd.h>

// Constructor
System::System()
{
}

// Destructor
System::~System()
{
}

SystemParameters & System::read()
{
    return System::currentParameters;
}

UpdateStatus System::write(SystemParameters const & params)
{
    this->currentParameters.node_id = params.node_id;
    this->currentParameters.system_name = params.system_name;
    // In order to create a blocking call, adding a time sleep.
    sleep(5);
    return DONE;
}
