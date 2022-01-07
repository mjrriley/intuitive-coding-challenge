#ifndef _EMBEDDED_H_
#define _EMBEDDED_H_

#include <stdint.h>
#include <string>

#define INVALID_ID      (255)

typedef struct
{
    uint8_t         node_id = INVALID_ID;
    std::string     system_name;
    uint64_t        system_time = 0;
    bool            active = false;
} SystemParameters;

typedef enum
{
    DONE = 0,
    FAILED = 1
} UpdateStatus;

class System
{
public:

    static System& getInstance()
    {
        static System instance;
        return instance;
    }

    UpdateStatus write(SystemParameters const & params);
    SystemParameters & read();

    System();
   ~System();

private:
    SystemParameters currentParameters;
};

#endif // _EMBEDDED_H_
