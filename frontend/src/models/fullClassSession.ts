import type { Attendance } from './attendance'
import type { ClassGroup } from './classGroup'
import type { Device } from './device'

export interface FullClassSession {
  id: string
  classgroupId: string
  roomDeviceId: string
  startTime: Date
  endTime: Date
  classgroup: ClassGroup
  roomDevice: Device
  attendances: Attendance[]
}
